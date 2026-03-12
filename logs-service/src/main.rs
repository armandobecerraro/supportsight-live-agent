//! CLI entry point for log parser.
mod parser;
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).expect("Failed to read stdin");
    let result = parser::parse_logs(&input);
    println!("{}", serde_json::to_string_pretty(&result).unwrap());
}
