`timescale 1ns / 1ps


module mux2la1(
    input in,
    input [7:0] A,
    input [7:0] B,
    output [7:0] out
    );
    
    assign out = in ? B : A;
    
endmodule
