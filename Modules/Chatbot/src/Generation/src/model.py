from transformers import GPT2TokenizerFast, GPT2Tokenizer, GPT2LMHeadModel, get_polynomial_decay_schedule_with_warmup
from anees_dataset import *
from preprocess import *
from tqdm import tqdm
from torch.utils.data import DataLoader
from torch.nn import functional as F
from torch.utils.tensorboard import SummaryWriter
from itertools import chain

import torch
import os
import sys
import numpy as np
import copy
import math
import random

SEED = 0


class AneesTrainer():
    def __init__(self, args):
        self.args = args

        if torch.cuda.is_available():
            self.args.device = torch.device(f"cuda:0")
        else:
            self.args.device = torch.device("cpu")

        print("Loading the tokenizer...")
        # self.tokenizer = GPT2TokenizerFast.from_pretrained(
        #     self.args.model_type)
        self.tokenizer = GPT2Tokenizer.from_pretrained(
            self.args.model_type)
        special_tokens = {
            'bos_token': self.args.bos_token,
            'additional_special_tokens': [self.args.sp1_token, self.args.sp2_token]
        }
        self.args.eos_token = self.tokenizer.eos_token
        _ = self.tokenizer.add_special_tokens(special_tokens)
        vocab = self.tokenizer.get_vocab()
        self.args.vocab_size = len(vocab)
        self.args.bos_id = vocab[self.args.bos_token]
        self.args.eos_id = vocab[self.args.eos_token]
        self.args.sp1_id = vocab[self.args.sp1_token]
        self.args.sp2_id = vocab[self.args.sp2_token]

        print("Loading the model...")
        self.set_seed(SEED)
        self.model = GPT2LMHeadModel.from_pretrained(
            self.args.model_type).to(self.args.device)
        self.model.resize_token_embeddings(self.args.vocab_size)

        self.args.max_len = min(self.args.max_len, self.model.config.n_ctx)

        if self.args.mode == 'train':
            print("Loading the optimizer...")
            self.optim = torch.optim.AdamW(
                self.model.parameters(), lr=self.args.lr)
            self.best_loss = sys.float_info.max
            self.last_epoch = 0

            print("Loading train & valid data...")
            train_set = AneesDataset(self.args.train_prefix, self.args)
            valid_set = AneesDataset(self.args.valid_prefix, self.args)

            self.train_loader = DataLoader(train_set,
                                           collate_fn=self.pad_collate,
                                           shuffle=True,
                                           batch_size=self.args.batch_size,
                                           num_workers=0,
                                           pin_memory=True)
            self.valid_loader = DataLoader(valid_set,
                                           collate_fn=self.pad_collate,
                                           batch_size=self.args.batch_size,
                                           num_workers=0,
                                           pin_memory=True)

            if not os.path.exists(self.args.ckpt_dir):
                os.makedirs(self.args.ckpt_dir)

            # Calculate total training steps
            num_batches = len(self.train_loader)
            args.total_train_steps = args.num_epochs * num_batches
            args.warmup_steps = int(args.warmup_ratio * args.total_train_steps)

            self.sched = get_polynomial_decay_schedule_with_warmup(
                self.optim,
                num_warmup_steps=args.warmup_steps,
                num_training_steps=args.total_train_steps,
                power=2
            )

            self.writer = SummaryWriter()

        if self.args.ckpt_name is not None:
            ckpt_path = f"{self.args.ckpt_dir}/{self.args.ckpt_name}.ckpt"
            if os.path.exists(ckpt_path):
                print("Loading the trained checkpoint...")
                ckpt = torch.load(ckpt_path, map_location=self.args.device)
                self.model.load_state_dict(ckpt['model_state_dict'])

                if self.args.mode == 'train':
                    print(
                        f"The training will start with the specified checkpoint: {self.args.ckpt_name}.ckpt.")
                    self.optim.load_state_dict(ckpt['optim_state_dict'])
                    self.sched.load_state_dict(ckpt['sched_state_dict'])
                    self.best_loss = ckpt['loss']
                    self.last_epoch = ckpt['epoch']
                else:
                    print("The interaction will start with the specified checkpoint.")
            else:
                print(f"Cannot find the specified checkpoint {ckpt_path}.")
                if self.args.mode == 'train':
                    print("Training will start from the begining.")
                else:
                    exit()

    def pad_collate(self, batch):
        input_ids, token_type_ids, labels = [], [], []
        for idx, seqs in enumerate(batch):
            input_ids.append(torch.LongTensor(seqs[0]))
            token_type_ids.append(torch.LongTensor(seqs[1]))
            labels.append(torch.LongTensor(seqs[2]))

        input_ids = torch.nn.utils.rnn.pad_sequence(
            input_ids, batch_first=True, padding_value=self.args.eos_id)
        token_type_ids = torch.nn.utils.rnn.pad_sequence(
            token_type_ids, batch_first=True, padding_value=self.args.eos_id)
        labels = torch.nn.utils.rnn.pad_sequence(
            labels, batch_first=True, padding_value=-100)

        return input_ids, token_type_ids, labels

    def train(self):
        self.set_seed(SEED)  # Set the seed for reproducibility
        print("Starting the training...")

        start_epoch = self.last_epoch+1
        for epoch in range(start_epoch, start_epoch+self.args.num_epochs):
            self.model.train()

            print(f"#"*50 + f"Epoch: {epoch}" + "#"*50)
            train_losses = []  # For the average loss
            train_ppls = []  # For the average perplexity
            for i, batch in enumerate(tqdm(self.train_loader)):
                input_ids, token_type_ids, labels = batch  # Get the data
                input_ids, token_type_ids, labels = \
                    input_ids.to(self.args.device), token_type_ids.to(
                        self.args.device), labels.to(self.args.device)  # Move to GPU

                outputs = self.model(
                    input_ids=input_ids,
                    token_type_ids=token_type_ids,
                    labels=labels
                )  # Forward pass

                # Get the loss and logits
                loss, logits = outputs[0], outputs[1]

                self.optim.zero_grad()  # Zero the gradients
                loss.backward()  # Backward pass
                self.optim.step()  # Update the parameters
                self.sched.step()  # Update the learning rate

                train_losses.append(loss.detach())  # Add the loss to the list
                ppl = torch.exp(loss.detach())  # Calculate the perplexity
                train_ppls.append(ppl)  # Add the perplexity to the list

            train_losses = [loss.item()
                            for loss in train_losses]  # Convert to numpy
            train_ppls = [ppl.item() if not math.isinf(
                ppl.item()) else 1e+8 for ppl in train_ppls]  # Convert to numpy
            train_loss = np.mean(train_losses)  # Calculate the average loss
            train_ppl = np.mean(train_ppls)  # Calculate the average perplexity
            print(f"Train loss: {train_loss} || Train perplexity: {train_ppl}")

            self.writer.add_scalar("Loss/train", train_loss, epoch)
            self.writer.add_scalar("PPL/train", train_ppl, epoch)

            self.last_epoch += 1

            # Calculate the validation loss and perplexity
            valid_loss, valid_ppl = self.validation()

            if valid_loss < self.best_loss:  # If the validation loss is better than the best loss
                self.best_loss = valid_loss
                state_dict = {
                    'model_state_dict': self.model.state_dict(),
                    'optim_state_dict': self.optim.state_dict(),
                    'sched_state_dict': self.sched.state_dict(),
                    'loss': self.best_loss,
                    'epoch': self.last_epoch
                }

                torch.save(
                    state_dict, f"{self.args.ckpt_dir}/best_ckpt_epoch={epoch}_valid_loss={round(self.best_loss, 4)}.ckpt")
                print("*"*10 + "Current best checkpoint is saved." + "*"*10)
                print(
                    f"{self.args.ckpt_dir}/best_ckpt_epoch={epoch}_valid_loss={round(self.best_loss, 4)}.ckpt")

            print(f"Best valid loss: {self.best_loss}")
            print(f"Valid loss: {valid_loss} || Valid perplexity: {valid_ppl}")

            self.writer.add_scalar("Loss/valid", valid_loss, epoch)
            self.writer.add_scalar("PPL/valid", valid_ppl, epoch)

            self.writer.add_scalars("Losses", {
                'train': train_loss,
                'valid': valid_loss,
            }, epoch)
            self.writer.add_scalars("PPLs", {
                'train': train_ppl,
                'valid': valid_ppl,
            }, epoch)

        print("Training finished.")

    def validation(self):
        print("Validation processing...")
        self.model.eval()

        valid_losses = []  # For the average loss
        valid_ppls = []  # For the average perplexity
        with torch.no_grad():  # No need to calculate the gradients
            for i, batch in enumerate(tqdm(self.valid_loader)):  # For each batch
                input_ids, token_type_ids, labels = batch  # Get the data
                input_ids, token_type_ids, labels = \
                    input_ids.to(self.args.device), token_type_ids.to(
                        self.args.device), labels.to(self.args.device)  # Move to GPU

                outputs = self.model(
                    input_ids=input_ids,
                    token_type_ids=token_type_ids,
                    labels=labels
                )  # Forward pass

                # Get the loss and logits
                loss, logits = outputs[0], outputs[1]

                valid_losses.append(loss.detach())  # Add the loss to the list
                ppl = torch.exp(loss.detach())  # Calculate the perplexity
                valid_ppls.append(ppl)  # Add the perplexity to the list

            valid_losses = [loss.item()
                            for loss in valid_losses]  # Convert to numpy
            valid_ppls = [ppl.item() if not math.isinf(
                ppl.item()) else 1e+8 for ppl in valid_ppls]  # Convert to numpy
            valid_loss = np.mean(valid_losses)  # Calculate the average loss
            valid_ppl = np.mean(valid_ppls)  # Calculate the average perplexity

            if math.isnan(valid_ppl):  # If the perplexity is NaN
                valid_ppl = 1e+8

        return valid_loss, valid_ppl

    def respond(self, utter, history=[]):
        with torch.no_grad():
            input_hists = [[self.args.sp1_id] + self.tokenizer.encode(res) if i % 2 == 0 else [
                self.args.sp2_id] + self.tokenizer.encode(self.args.encode_prefix + res) for i, res in enumerate(history)]
            utter = preprocess(utter)
            input_ids = [self.args.sp1_id] + \
                self.tokenizer.encode(self.args.encode_prefix + utter)
            input_hists.append(input_ids)

            if len(input_hists) >= self.args.max_turns:
                num_exceeded = len(input_hists) - self.args.max_turns + 1
                input_hists = input_hists[num_exceeded:]

            input_ids = [self.args.bos_id] + \
                list(chain.from_iterable(input_hists)) + [self.args.sp2_id]

            start_sp_id = input_hists[0][0]
            next_sp_id = self.args.sp1_id if start_sp_id == self.args.sp2_id else self.args.sp2_id
            assert start_sp_id != next_sp_id

            token_type_ids = [[start_sp_id] * len(hist) if h % 2 == 0 else [
                next_sp_id] * len(hist) for h, hist in enumerate(input_hists)]
            assert len(token_type_ids) == len(input_hists)

            token_type_ids = [
                start_sp_id] + list(chain.from_iterable(token_type_ids)) + [self.args.sp2_id]
            assert len(input_ids) == len(token_type_ids)
            input_len = len(input_ids)

            input_ids = torch.LongTensor(
                input_ids).unsqueeze(0).to(self.args.device)
            token_type_ids = torch.LongTensor(
                token_type_ids).unsqueeze(0).to(self.args.device)

            output_ids = self.nucleus_sampling(
                input_ids, token_type_ids, input_len)
            res = self.tokenizer.decode(
                output_ids, skip_special_tokens=True)

            return res.replace(self.args.encode_prefix, '')

    def interact(self):
        print("Start interaction...")
        print(
            f"To end the conversation, please type \"{self.args.end_command}\".")
        self.model.eval()
        self.set_seed(SEED)

        with torch.no_grad():
            input_hists = []  # For the input history

            while True:
                utter = input("أنت: ")
                if utter == self.args.end_command:
                    print("أنيس: إلى اللقاء")
                    break
                utter = preprocess(utter)  # Preprocess the utterance
                input_ids = [self.args.sp1_id] + \
                    self.tokenizer.encode(self.args.encode_prefix + utter)
                input_hists.append(input_ids)

                # If the number of turns is greater than the maximum turns
                if len(input_hists) >= self.args.max_turns:
                    # Calculate the number of exceeded turns
                    num_exceeded = len(input_hists) - self.args.max_turns + 1
                    # Remove the exceeded turns
                    input_hists = input_hists[num_exceeded:]

                input_ids = [self.args.bos_id] + \
                    list(chain.from_iterable(input_hists)) + \
                    [self.args.sp2_id]  # Concatenate the input history
                # Get the start special token id
                start_sp_id = input_hists[0][0]
                # Get the next special token id
                next_sp_id = self.args.sp1_id if start_sp_id == self.args.sp2_id else self.args.sp2_id
                assert start_sp_id != next_sp_id  # Check the start and next special token id
                token_type_ids = [[start_sp_id] * len(hist) if h % 2 == 0 else [
                    next_sp_id] * len(hist) for h, hist in enumerate(input_hists)]  # Calculate the token type ids
                # Check the length of token type ids
                assert len(token_type_ids) == len(input_hists)
                token_type_ids = [
                    start_sp_id] + list(chain.from_iterable(token_type_ids)) + [self.args.sp2_id]  # Concatenate the token type ids
                # Check the length of input ids and token type ids
                assert len(input_ids) == len(token_type_ids)
                input_len = len(input_ids)  # Calculate the length of input ids

                input_ids = torch.LongTensor(
                    input_ids).unsqueeze(0).to(self.args.device)  # Convert to tensor
                token_type_ids = torch.LongTensor(
                    token_type_ids).unsqueeze(0).to(self.args.device)  # Convert to tensor

                output_ids = self.nucleus_sampling(
                    input_ids, token_type_ids, input_len)  # Get the output ids
                res = self.tokenizer.decode(
                    output_ids, skip_special_tokens=True)  # Decode the output ids

                print(f"أنيس: {res.replace(self.args.encode_prefix, '')}")
                input_hists.append([self.args.sp2_id] +
                                   self.tokenizer.encode(res))  # Add the output to the input history

    # Nucleus sampling
    def nucleus_sampling(self, input_ids, token_type_ids, input_len):
        output_ids = []  # For the output ids
        for pos in range(input_len, self.args.max_len):  # For each position
            output = self.model(input_ids=input_ids, token_type_ids=token_type_ids)[
                0][:, pos-1]  # (1, V) Get the output at the position
            output = F.softmax(output, dim=-1)  # (1, V) Softmax the output

            sorted_probs, sorted_idxs = torch.sort(
                output, descending=True)  # Sort the output
            # Calculate the cumsum of the output
            cumsum_probs = torch.cumsum(sorted_probs, dim=-1)
            idx_remove = cumsum_probs > self.args.top_p  # Calculate the idx to remove
            # Clone the idx to remove
            idx_remove[:, 1:] = idx_remove[:, :-1].clone()
            idx_remove[:, 0] = False  # Set the first idx to False
            sorted_probs[idx_remove] = 0.0  # Set the removed idx to 0.0
            sorted_probs /= torch.sum(sorted_probs,
                                      dim=-1, keepdim=True)  # Normalize the output

            probs = torch.zeros(
                output.shape, device=self.args.device).scatter_(-1, sorted_idxs, sorted_probs)  # Get the probs
            idx = torch.multinomial(probs, 1)  # (1, 1) Get the idx

            idx_item = idx.squeeze(-1).squeeze(-1).item()  # Get the idx item
            output_ids.append(idx_item)  # Add the idx to the output ids

            if idx_item == self.args.eos_id:  # If the idx is the end of sentence id
                break

            # Add the idx to the input ids
            input_ids = torch.cat((input_ids, idx), dim=-1)
            next_type_id = torch.LongTensor(
                [[self.args.sp2_id]]).to(self.args.device)  # (1, 1) Get the next special token id
            # Add the next special token id to the token type ids
            token_type_ids = torch.cat((token_type_ids, next_type_id), dim=-1)
            # Check the shape of input ids and token type ids
            assert input_ids.shape == token_type_ids.shape

        return output_ids

    def set_seed(self, seed):
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        random.seed(seed)
