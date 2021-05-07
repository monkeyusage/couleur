mod files;
mod img;

use rayon::prelude::*;
use std::vec;

mod resize {
    fn resize() {
        let files = files::read_img_paths(r"data\img").unwrap();
        let _images: vec::Vec<()> = files
            .par_iter()
            .map(|f| img::resize(f.to_path_buf()))
            .collect();
    }
}


mod kmeans {
    fn kmeans() {
        let files = files::read_img_paths(r"data\transforms");
        for file in files {
            let data = img::read(file);
            let mut mean : f32 = 0;
            for pixel in data {
                mean += pixel;
            }
        }
    }
}