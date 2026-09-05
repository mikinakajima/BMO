#!/usr/bin/env python3
import os
import dill as pkl

FILES = [
    "thermal.pkl",
    "buoyancy.pkl",
    "magnetic_nominal.pkl",
    "entropy_nominal.pkl",
    "param.pkl",
]

DEMO_DIR = "Demo"

def describe(name, obj):
    print("\n" + "=" * 70)
    print(name)
    print("TYPE:", type(obj))

    if isinstance(obj, dict):
        print("KEYS:")
        for k, v in obj.items():
            shape = getattr(v, "shape", None)
            if shape is not None:
                print(f"  {k:30s} shape={shape}")
            else:
                print(f"  {k:30s} type={type(v).__name__}")
        return

    if hasattr(obj, "__dict__"):
        print("ATTRIBUTES:")
        for k, v in obj.__dict__.items():
            shape = getattr(v, "shape", None)
            if shape is not None:
                print(f"  {k:30s} shape={shape}")
            else:
                print(f"  {k:30s} type={type(v).__name__}")
        return

    print("VALUE:")
    print(obj)

for filename in FILES:
    path = os.path.join(DEMO_DIR, filename)

    if not os.path.exists(path):
        print(f"\nSkipping {path}: file not found")
        continue

    try:
        with open(path, "rb") as f:
            obj = pkl.load(f)
        describe(path, obj)
    except Exception as e:
        print(f"\nCould not read {path}")
        print(type(e).__name__ + ":", e)
