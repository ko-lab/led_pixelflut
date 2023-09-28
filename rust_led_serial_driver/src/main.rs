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
use std::thread::sleep;
use serialport::SerialPort;


fn main() {
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }
    let mut port = serialport::new("/dev/ttyACM1", 115_200)
        .timeout(Duration::from_millis(10))
        .open().expect("Failed to open port");
    while (true) {
        full_display_color_cycle(&mut port);
    }
}

fn full_display_color_cycle(mut port: &mut Box<dyn SerialPort>) {
    for i in 0..256 {
        send_pixel(&mut port, 0, 64, 0);
    }
    const WAIT_TIME: u64 = 100;
    sleep(Duration::from_millis(WAIT_TIME));
    for i in 0..256 {
        send_pixel(&mut port, 0, 0, 64);
    }
    sleep(Duration::from_millis(WAIT_TIME));
    for i in 0..256 {
        send_pixel(&mut port, 64, 0, 0);
    }
    sleep(Duration::from_millis(WAIT_TIME));
}

fn send_pixel<W>(writer: &mut W, r: u8, g: u8, b: u8)
    where
        W: Write {
    write_8_bit_number(writer, r);
    write_8_bit_number(writer, g);
    write_8_bit_number(writer, b);
}
