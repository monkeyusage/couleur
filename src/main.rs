use image;
use image::io::Reader as ImageReader;
use std::{fs, io, path, vec};
use rayon::prelude::*;

fn read_dir(path: path::PathBuf) -> io::Result<vec::Vec<path::PathBuf>> {
    let items = fs::read_dir(path)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;
    Ok(items)
}

fn read_img_paths() -> io::Result<vec::Vec<path::PathBuf>> {
    let mut files: vec::Vec<path::PathBuf> = vec::Vec::new();
    let dirs = read_dir(path::PathBuf::from(r"data\img"))?;
    for dir in &dirs {
        if dir.is_dir() {
            let inner_dirs = read_dir(dir.to_path_buf())?;
            for file in &inner_dirs {
                if file.is_file() && file.extension().unwrap() == "jpg" {
                    files.push(file.to_path_buf());
                } else {
                    println!("{} not recognized", file.display());
                }
            }
        }
    }
    println!("{} files in the vector", files.len());
    Ok(files)
}

fn process_img(file: path::PathBuf) -> () {
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

fn main() {
    let files = read_img_paths().unwrap();
    let _images : vec::Vec<()> = files.par_iter().map(|f| {
        process_img(f.to_path_buf())
    }).collect();
}
