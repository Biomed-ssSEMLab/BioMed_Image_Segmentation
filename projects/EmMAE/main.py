import os
import torch

from connectomics.utils.system import get_args, init_devices
from connectomics.config import load_cfg, save_all_cfg
from engine.trainer import TrainerMAE
from engine.config import add_MAE_config

def main():
    args = get_args()
    cfg = load_cfg(args, freeze=False, add_cfg_func=add_MAE_config)
    device = init_devices(args, cfg)

    if args.local_rank == 0 or args.local_rank is None:
        # In distributed training, only print and save the configurations
        # using the node with local_rank=0.
        print("PyTorch: ", torch.__version__)
        print(cfg)

        if not os.path.exists(cfg.DATASET.OUTPUT_PATH):
            print('Output directory: ', cfg.DATASET.OUTPUT_PATH)
            os.makedirs(cfg.DATASET.OUTPUT_PATH)
            save_all_cfg(cfg, cfg.DATASET.OUTPUT_PATH)

    # start training or inference
    mode = 'test' if args.inference else 'train'
    trainer = TrainerMAE(cfg, device=device, mode=mode, rank=args.local_rank,checkpoint=args.checkpoint)

    # Start training or inference:
    trainer.test() if args.inference else trainer.train()
    print("Rank: {}. Device: {}. Process is finished!".format(args.local_rank, device))


if __name__ == "__main__":
    main()