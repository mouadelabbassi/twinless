import argparse
import json
from .mission import run_mission


def main():
    parser = argparse.ArgumentParser(description="TWINLESS: deterministic foundation")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--noise", type=float, default=0.0,
                        help="Gaussian voltage measurement noise std (V)")
    args = parser.parse_args()
    print(json.dumps(run_mission(seed=args.seed, noise_std=args.noise), indent=2))


if __name__ == "__main__":
    main()
