`timescale 1ns / 1ps


module simulare;

    reg [7:0] N, D;
    wire[7:0] R, Q;
    reg start, reset, clk;
    wire done, idle;
    
    final u(clk, N, D, Q, R, start, reset, idle, done);
    
    integer i;
    
    initial begin
        clk = 0;
        start = 0;
        reset = 0;
        N = 44;
        D = 6;
        #1;
        
        reset = 1;
        #1;
        reset = 0;
        
        start = 1;
        clk = 1;
        #3;
        clk = 0;
        start = 0;
        #3;
        
        for (i = 0; i < 100; i = i + 1) begin
            clk = 1;
            #3;
            clk = 0;
            #3;
        end
    end
endmodule
