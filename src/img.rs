use image;
use image::io::Reader as ImageReader;
use smartcore::cluster::kmeans::*;
use smartcore::linalg::naive::dense_matrix::*;
use std::{path, vec};

pub fn resize(file: path::PathBuf) {
    let mut img = ImageReader::open(&file).unwrap().decode().unwrap();
    img = img.resize(200, 200, image::imageops::FilterType::Nearest);
    let file_str = &file.into_os_string().into_string().unwrap();
    let mut file_path: vec::Vec<&str> = file_str.split(r"\").collect();
    let file_name = file_path.pop().unwrap();
    let dir_name = file_path.pop().unwrap();
    let path_name = format!("data\\transforms\\{}\\{}", dir_name, file_name);
    println!("Saving new image on to path {}", &path_name);
    img.save(path_name).unwrap();
}

pub fn measure(file: path::PathBuf) -> f32 {
    let img = ImageReader::open(&file).unwrap().decode().unwrap();
    let pixels = img.as_rgb16().unwrap().to_vec();
    let mut total : u16 = 0;
    for pixel in pixels {
        total += pixel;
    };
    total / pixels.len()
}
