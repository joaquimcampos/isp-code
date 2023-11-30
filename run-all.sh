#!/bin/bash

assets_dir=assets-superres-resized
for img_path in "$assets_dir"/*
do
  tmp="$(cut -d'.' -f1 <<<"$img_path")"
  base_filename="$(cut -d'/' -f2 <<<"$tmp")"
  outdir=output_zoom/"$base_filename"
  python3 face_video_zoom.py $img_path --outdir $outdir
done
