`timescale 1ns / 1ps

module comanda(
    input clk,
    input reset,
    input start,
    output reg done,
    output reg idle,
    output reg sel_M1,
    output reg sel_M2,
    output reg sel_M3,
    output reg [1:0] sel_M4,
    input flag,
    output reg B,
    output reg [2:0] op,
    output reg [7:0] imm,
    output reg [1:0] selA,
    output reg wrA,
    output reg [1:0] selB,
    output reg wrB
    );


    reg [3:0] state;
    reg [2:0] i;
    
    
    always @(posedge reset) begin
        sel_M1 <= 0;
        sel_M2 <= 1;
        sel_M3 <= 0;
        sel_M4 <= 2;
        
        state <= 0;
        done <= 0;
        idle <= 1;
        
        B <= 0;
        op <= 0;
        imm <= 0;
        
        selA <= 0;
        wrA <= 0;
        selB <= 0;
        wrB <= 0;
    end
    
    
    always @(*) begin
        case(state)
            0: begin
                selA <= 1;
                selB <= 0;
                idle <= 1;
                done <= 0;
                wrB <= 0;
            end
            
            1: begin
                idle <= 0;
                sel_M1 <= 0;
                op <= 1;
                done <= flag ? 1 : 0;
                wrB <= 0;
            end
            
            2: begin
                selA <= 0;
                selB <= 1;
                sel_M3 <= 1;
                wrA <= 1;
                wrB <= 1;
            end
            
            3: begin
                selB <= 3;
                wrA <= 0;
                wrB <= 1;
            end
            
            4: begin
                selB <= 0;
                sel_M1 <= 1;
                op <= 2;
                sel_M3 <= 0;
                wrB <= 1;
            end
            
            5: begin
                selB <= 2;
                sel_M3 <= 1;
                imm <= i;
                wrB <= 1;
            end
            
            6: begin
                imm <= 0;
                sel_M1 <= 1;
                wrB <= 0;
                op <= 3;
                sel_M2 <= 0;
            end
            
            7: begin
                op <= 4;
                selB <= 0;
                wrB <= 1;
                sel_M3 <= 0;
                selA <= 3;
                sel_M2 <= 1;
            end
            
            8: begin
                wrB <= 0;
                sel_M1 <= 0;
                selA <= 0;
                op <= 5;
            end
            
            9: begin
                op <= 6;
                wrB <= 1;
            end
            
            10: begin
                sel_M1 <= 1;
                selB <= 1;
                selA <= 2;
                op <= 4;
                wrB <= 1;
            end
            
            11: begin
                selB <= 0;
                wrB <= 0;
            end
            
            12: begin
                selA <= i == 7;
                done <= i == 7;
                wrB <= 0;
            end
        endcase
    end
    
    always @(posedge clk) begin
        case(state)
            0:  state <= start ? 1 : 0;
            
            1:  begin
                    state <= flag ? 0 : 2;
                    i <= 7;
                end
                
            6:  begin
                    state <= state + 1;
                    B <= flag;
                end
                
            8:  begin
                    B <= 1;
                    state <= flag ? 9 : 11;
                end
                
            11: begin
                    i <= i - 1;
                    state <= state + 1;
                end
                
            12: state <= i == 7 ? 0 : 3;
            
            default: state <= state + 1;
        endcase
    end
    
endmodule