`timescale 1ns / 1ps


module caledate(
    input clk,
    input sel_M1,
    input sel_M2,
    input sel_M3,
    input [1:0] sel_M4,
    input [7:0] N,
    input [7:0] D,
    input [2:0] op,
    input [7:0] imm,
    input [1:0] selA,
    input [1:0] selB,
    input wrA,
    input wrB,
    input B,
    output flag,
    output [7:0] Q,
    output [7:0] R
    );
    
    
    wire [7:0] wireA;
    wire [7:0] wireC;
    wire [7:0] wireD;
    wire [7:0] wireMB;
    wire [7:0] wireMA;
    
    
    mux2la1 mux1(sel_M1, D, R, wireA);
    mux2la1 mux2(sel_M2, N, Q, wireC);
    mux2la1 mux3(sel_M3, wireD, imm, wireMB);
    mux4la1 mux4(sel_M4, N, D, imm, imm, wireMA);
    
    
    alu a(wireA, B, wireC, wireD, op, flag);
    registri r(clk, wireMA, selA, wrA, wireMB, selB, wrB, Q, R);
    
endmodule
