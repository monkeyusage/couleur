mod files;
mod img;

use rayon::prelude::*;
use std::vec;

fn main() {
    let files = files::read_img_paths(r"data\transform").unwrap();
    let _images: vec::Vec<()> = files
        .par_iter()
        .map(|f| img::resize(f.to_path_buf()))
        .collect();
}
