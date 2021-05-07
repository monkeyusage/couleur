mod files;
mod img;

// use rayon::prelude::*;
use std::vec;

struct ImageBuf {
    red : vec::Vec<u8>,
    green : vec::Vec<u8>,
    blue : vec::Vec<u8>
}

impl ImageBuf {
    fn new() -> Self {
        ImageBuf {
            red : vec::Vec::new(),
            green : vec::Vec::new(),
            blue : vec::Vec::new()
        }
    }

    fn from(data: image::ImageBuffer<image::Rgb<u8>, std::vec::Vec<u8>>) -> Self {
        let mut img_buf = ImageBuf::new();
        for &pixel in data.pixels() {
            img_buf.push(pixel);
        }
        img_buf
    }

    fn push(&mut self, pixel : image::Rgb<u8>) ->  &Self {
        self.red.push(pixel[0]);
        self.green.push(pixel[1]);
        self.blue.push(pixel[2]);
        self
    }


    fn mean(&self) -> [u8; 3] {
        let result = [0, 0, 0];
        result
    }
}



fn main() {
    let file_paths = files::read_img_paths(r"data\transforms").unwrap();
    for file in file_paths {
        let data = img::read(file.to_path_buf());
        let len = data.len();
        let mut _img_buf = ImageBuf::from(data);
        println!("len {}, file {}", len, file.display());
    }
}
