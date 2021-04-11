`timescale 1ns / 1ps


module final(
    input clk,
    input [7:0] N,
    input [7:0] D,
    output [7:0] Q,
    output [7:0] R,
    input start,
    input reset,
    output idle,
    output done
    );
    
    
    wire [2:0] op;
    wire [7:0] imm;
    wire [1:0] selA;
    wire [1:0] selB;
    wire sel_M1;
    wire sel_M2;
    wire sel_M3;
    wire [1:0] sel_M4;
    wire wrA;
    wire wrB;
    wire flag;
    wire B;
    
    
    caledate data(clk, sel_M1, sel_M2, sel_M3, sel_M4, N, D, op, imm, selA, selB, wrA, wrB, B, flag, Q, R);
    comanda control(clk, reset, start, done, idle, sel_M1, sel_M2, sel_M3, sel_M4, flag, B, op, imm, selA, wrA, selB, wrB);
    
endmodule
