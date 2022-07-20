from torch.utils.data import Dataset
from tqdm import tqdm
from itertools import chain

import torch
import copy
import json


class AneesDataset(Dataset):
    def __init__(self, prefix, args):
        assert prefix == args.train_prefix or prefix == args.valid_prefix

        print(f"Loading {prefix}_id.json...")
        with open(f"{args.data_dir}/{prefix}_ids.json", 'r') as f:
            dials = json.load(f)

        self.input_ids = []  # (N, L)
        self.token_type_ids = []  # (N, L)
        self.labels = []  # (N, L)

        print(f"Processing {prefix} data...")
        for dial in tqdm(dials):
            hists = []
            # Append speaker token to the beginning of each history
            for u, utter in enumerate(dial):
                if u % 2 == 0:
                    hists.append([args.sp1_id] + utter)
                else:
                    hists.append([args.sp2_id] + utter)

            for h in range(len(hists)):
                if hists[h][0] == args.sp2_id:  # if speaker is sp2
                    # start index of the current turn
                    start = max(0, h-args.max_turns+1)
                    for s in range(start, h):  # for each turn before the current turn
                        contexts = hists[s:h+1]  # contexts of the current turn
                        input_ids = [
                            args.bos_id] + list(chain.from_iterable(contexts)) + [args.eos_id]  # concatenate all the contexts
                        if len(input_ids) <= args.max_len:
                            # start and next speaker ids
                            start_sp_id, next_sp_id = contexts[0][0], contexts[1][0]
                            token_type_ids = [[start_sp_id] * len(ctx) if c % 2 == 0 else [
                                next_sp_id] * len(ctx) for c, ctx in enumerate(contexts)]  # token type ids
                            # last token type id should be sp2
                            assert token_type_ids[-1][0] == args.sp2_id
                            token_type_ids = [
                                start_sp_id] + list(chain.from_iterable(token_type_ids)) + [args.sp2_id]  # concatenate all the token type ids
                            # input ids and token type ids should have the same length
                            assert len(input_ids) == len(token_type_ids)

                            labels = [[-100] * len(ctx) if c < len(
                                contexts)-1 else [-100] + ctx[1:] for c, ctx in enumerate(contexts)]  # labels
                            # last labels should be the same as the last context
                            assert labels[-1][1:] == contexts[-1][1:]
                            labels = [-100] + \
                                list(chain.from_iterable(labels)) + \
                                [args.eos_id]  # concatenate all the labels
                            # input ids and labels should have the same length
                            assert len(input_ids) == len(labels)

                            self.input_ids.append(
                                input_ids)  # append input ids
                            self.token_type_ids.append(
                                token_type_ids)  # append token type ids
                            self.labels.append(labels)  # append labels

                            break

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.token_type_ids[idx], self.labels[idx]
