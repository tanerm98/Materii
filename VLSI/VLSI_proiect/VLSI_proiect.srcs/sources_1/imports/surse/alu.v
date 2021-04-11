`timescale 1ns / 1ps


module alu(
    input [7:0] A,
    input B,
    input [7:0] C,
    output reg [7:0] D,
    input [2:0] op,
    output reg flag
    );


    always @(*) begin
        case(op)
            0: begin
                flag <= 0;
                D <= 0;
            end
            1: begin
                flag <= (A == 0);
                D <= 0;
            end
            2: begin
                flag <= 0;
                D <= A << 1;
            end
            3: begin
                flag <= C[A];
                D <= 0;
            end
            4: begin
                flag <= 0;
                D <= A;
                D[C] <= B;
            end
            5: begin
                flag <= (C >= A);
                D <= 0;
            end
            6: begin
                flag <= 0;
                D <= C - A;
            end
            7: begin
                flag <= 0;
                D <= 0;
            end
        endcase
    end

endmodule
