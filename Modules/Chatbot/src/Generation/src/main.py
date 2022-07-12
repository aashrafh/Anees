

import argparse
from model import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--mode', type=str, required=True,
                        help="train or interact?")
    parser.add_argument('--ckpt_name', type=str, required=False,
                        help="The trained checkpoint without extension")

    parser.add_argument('--data_dir', type=str, default="data",
                        help="The data directory")
    parser.add_argument('--train_prefix', type=str, default="train",
                        help="The prefix of the train data files' name.")
    parser.add_argument('--valid_prefix', type=str, default="valid",
                        help="The prefix of the validation data files' name.")
    parser.add_argument('--encode_prefix', type=str, default="",
                        help="The prefix of the encode function used in tokenization.")
    parser.add_argument('--model_type', type=str,
                        default="aubmindlab/aragpt2-base", help="The name of the model of a path to local trained model")
    parser.add_argument('--bos_token', type=str,
                        default="<bos>", help="The begining of sentence token.")
    parser.add_argument('--sp1_token', type=str,
                        default="<sp1>", help="The speaker1 token.")
    parser.add_argument('--sp2_token', type=str,
                        default="<sp2>", help="The speaker2 token.")
    parser.add_argument('--lr', type=float, default=2e-5,
                        help="The learning rate.")
    parser.add_argument('--warmup_ratio', type=float, default=0.1,
                        help="The ratio of warmup steps to the total training steps.")
    parser.add_argument('--batch_size', type=int,
                        default=8, help="The batch size.")
    parser.add_argument('--num_epochs', type=int, default=10,
                        help="The number of total epochs.")
    parser.add_argument('--max_len', type=int, default=1024,
                        help="The maximum length of input sequence.")
    parser.add_argument('--max_turns', type=int, default=5,
                        help="The maximum number of dialogue histories to include.")
    parser.add_argument('--top_p', type=float, default=0.9,
                        help="The top-p value for nucleus sampling decoding.")
    parser.add_argument('--ckpt_dir', type=str, default="saved_models",
                        help="The directory name for saved checkpoints.")
    parser.add_argument('--end_command', type=str, default="EOC",
                        help="The command to end the conversation.")

    args = parser.parse_args()
    tainer = AneesTrainer(args)

    if args.mode == 'train':
        tainer.train()
    elif args.mode == 'interact':
        assert args.ckpt_name is not None, "Please specify the trained model checkpoint."
        tainer.interact()
