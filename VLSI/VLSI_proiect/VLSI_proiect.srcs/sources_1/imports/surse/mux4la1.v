`timescale 1ns / 1ps


module mux4la1(
    input [1:0] in,
    input [7:0] A,
    input [7:0] B,
    input [7:0] C,
    input [7:0] D,
    input [7:0] out
    );
    
    assign out = in[1] ? (in[0] ? D : C) : (in[0] ? B : A);
    
endmodule
