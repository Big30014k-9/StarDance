# Weird Storage

A Python script that turns any file into an image, packing its binary data into pixels, and allowing you to recover the original file later.

## What it does

**Weird Storage** acts as a simple file-to-image encoder and decoder. It takes any file (whether it's a text file, a script, or an archive), wraps it with a custom header containing its name and size, and converts those bytes into the pixels of a square PNG image. You can later reverse the process to completely restore your original file.

---

## How it works

The script relies on four core functions and a command-line interface:

1. **`pack(path)`**: Reads the target file's raw bytes and adds a custom binary header (`WSTR` magic bytes, filename length, and the filename itself) followed by the actual data.
2. **`encode(blob, out)`**: Calculates the dimensions needed for a square image to hold all those bytes (3 bytes per pixel for RGB), pads any leftover space with zeros, and uses the **Pillow** library to save it as a PNG image.
3. **`decode(path)` & `unpack(blob)`**: Opens the image, reads the pixels back into a byte stream, verifies the `WSTR` signature, extracts the filename, and reconstructs the original file inside a `recovered/` folder.
4. **`main()`**: Provides an interactive command-line interface (CLI) to choose between encoding (`c`) or decoding (`d`).

---

## Requirements

Make sure you have Python installed along with the **Pillow** library for image processing:

```bash
pip install Pillow
