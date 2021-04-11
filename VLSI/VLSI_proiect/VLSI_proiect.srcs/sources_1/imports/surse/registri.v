`timescale 1ns / 1ps


module registri(
    input clk,
    input [7:0] inA,
    input [1:0] selA,
    input wrA,
    input [7:0] inB,
    input [1:0] selB,
    input wrB,
    output reg [7:0] Q,
    output reg [7:0] R
    );
    
    
    reg [7:0] R0;
    reg [7:0] R1;
    reg [7:0] R2;
    reg [7:0] R3;
    
    
    always @(posedge clk) begin
        if (wrA) begin
            case (selA)
                2'b00: R0 <= inA;
                2'b01: R1 <= inA;
                2'b10: R2 <= inA;
                2'b11: R3 <= inA;
            endcase
        end
        
        if (wrB) begin
            case (selB)
                2'b00: R0 <= inB;
                2'b01: R1 <= inB;
                2'b10: R2 <= inB;
                2'b11: R3 <= inB;
            endcase
         end
    end
    
    
    always @(*) begin
        case(selA)
            0: Q = R0;
            1: Q = R1;
            2: Q = R2;
            3: Q = R3;
        endcase
    end
    
    always @(*) begin
        case(selB)
            0: R = R0;
            1: R = R1;
            2: R = R2;
            3: R = R3;
        endcase
    end
   
endmodule
