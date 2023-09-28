extern crate rand;
extern crate serialport;

use rand::Rng;
use std::time::Duration;
use std::io::{self, Read, Write, BufRead, BufReader};

fn write_8_bit_number(port: &mut Box<dyn SerialPort>, number: u8) -> io::Result<()>
{
    // Write the 8-bit number to the port
    port.write_all(&[number])?;
    // Wait for a response
    Ok(())
}

use std::{thread, time};
use std::thread::sleep;
use serialport::{FlowControl, SerialPort};


fn main() {
    let ports = serialport::available_ports().expect("No ports found!");
    for p in ports {
        println!("{}", p.port_name);
    }
    let mut port = serialport::new("/dev/ttyACM1", 115_200)
        .timeout(Duration::from_millis(100)).flow_control(FlowControl::None)
        .open().expect("Failed to open port");

    while (true) {
        full_display_color_cycle(&mut port);
    }
}

fn full_display_color_cycle(mut port: &mut Box<dyn SerialPort>) {
    for i in 0..256 {
        send_pixel(&mut port, 0, 64, 0);
    }
    const WAIT_TIME: u64 = 0;
    let mut buffer: [u8; 1] = [0; 1];
    sleep(Duration::from_millis(WAIT_TIME));
    port.read(&mut buffer).expect("read_to_string failed");

    for i in 0..256 {
        send_pixel(&mut port, 0, 0, 64);
    }
    port.read(&mut buffer).expect("read_to_string failed");
    sleep(Duration::from_millis(WAIT_TIME));

    for i in 0..256 {
        send_pixel(&mut port, 64, 0, 0);
    }
    port.read(&mut buffer).expect("read_to_string failed");
    sleep(Duration::from_millis(WAIT_TIME));
}

fn send_pixel(mut port: &mut Box<dyn SerialPort>, r: u8, g: u8, b: u8)
{
    write_8_bit_number(port, r);
    write_8_bit_number(port, g);
    write_8_bit_number(port, b);
}
