extern crate rand;                                                                                                                                                                                 
extern crate serialport;                                                                                                                                                                           
                                                                                                                                                                                                    
use rand::Rng;                                                                                                                                                                                     
use std::time::Duration;
use std::io::{self, Write};

fn write_8_bit_number<W>(writer: &mut W, number: u8) -> io::Result<()>
where
    W: Write,
{
    // Write the 8-bit number to the writer
    writer.write_all(&[number])?;
    Ok(())
}
use std::{thread, time};


fn main(){
let ten_millis = time::Duration::from_millis(1000);
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }
    let mut port = serialport::new("/dev/ttyACM1",115_200)
        .timeout(Duration::from_millis(10))
        .open().expect("Failed to open port");
    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 1);

    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 1);

    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 1);

    thread::sleep(ten_millis);

    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 1);

    write_8_bit_number(&mut port, 100);
    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 1);

    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 1);
    write_8_bit_number(&mut port, 100);
}
