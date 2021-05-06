use std::{fs, io, vec, path};
use image::io::Reader as ImageReader;

fn read_dir(path: path::PathBuf) -> io::Result<vec::Vec<path::PathBuf>> {
    let items = fs::read_dir(path)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;
    Ok(items)
}

fn read_img_paths() -> io::Result<vec::Vec<path::PathBuf>> {
    let mut files : vec::Vec<path::PathBuf> = vec::Vec::new();
    let dirs = read_dir(path::PathBuf::from(r"data\img"))?;
    for dir in &dirs {
        if dir.is_dir() {
            let inner_dirs = read_dir(dir.to_path_buf())?;
            for file in &inner_dirs {
                files.push(file.to_path_buf());
            }
        }
    };
    println!("{} files in the vector", files.len());
    Ok(files)
}

fn main() -> Result<(), image::ImageError> {
    let files = read_img_paths()?; 
    for file in files {
        println!("{}", file.display());
        let mut img = ImageReader::open(&file)?.decode()?;
        img = img.resize(200, 200, image::imageops::FilterType::Nearest);
        img.save(format!("{}_new.jpg", &file.display()))?;
        break
    }
    Ok(())
}