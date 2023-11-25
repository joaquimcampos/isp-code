#!/bin/bash

assets_dir=assets
for img_path in "$assets_dir"/*
do
  tmp="$(cut -d'.' -f1 <<<"$img_path")"
  base_filename="$(cut -d'/' -f2 <<<"$tmp")"
  outdir=output/"$base_filename"
  python3 face_video.py $img_path --duration 10 --outdir $outdir
done
