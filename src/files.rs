use std::{fs, io, path, vec};

pub fn read_dir(path: path::PathBuf) -> io::Result<vec::Vec<path::PathBuf>> {
    let items = fs::read_dir(path)?
        .map(|res| res.map(|e| e.path()))
        .collect::<Result<Vec<_>, io::Error>>()?;
    Ok(items)
}

pub fn read_img_paths(path_str: &str) -> io::Result<vec::Vec<path::PathBuf>> {
    let mut files: vec::Vec<path::PathBuf> = vec::Vec::new();
    let dirs = read_dir(path::PathBuf::from(path_str))?;
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
