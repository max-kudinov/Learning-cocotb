module tinyalu (
    // input  logic        clk,
    input  logic        reset_n,
    input  logic        start,
    input  logic [7:0]  A,
    input  logic [7:0]  B,
    input  logic [2:0]  op,
    output logic        done,
    output logic [15:0] result
);

    bit clk;
    initial clk = 0;
    always #5 clk = ~clk;

    logic [15:0] tmp_res;
    logic [15:0] alu_out;
    logic [1:0] cnt;
    parameter MAX = 2;

    typedef enum {
        READY,
        WAIT,
        OUTPUT
    } state_t;

    state_t state, next;

    always_ff @(posedge clk)
        if (!reset_n)
            state <= READY;
        else
            state <= next;

    always_comb begin
        next = state;

        case (state)
            READY: begin
                if (start == 1'b1) begin
                    if (op == 3'b100) next = WAIT;
                    else              next = OUTPUT;
                end
            end
            WAIT: begin
                if (cnt == MAX) next = OUTPUT;
            end
            OUTPUT: next = READY;
        endcase
    end

    always_ff @(posedge clk)
        if (!reset_n)
            cnt <= '0;
        else if (state != WAIT)
            cnt <= '0;
        else
            cnt <= cnt + 1'b1;

    always_comb begin
        case (op)
            3'b001: alu_out = 16'(A) + 16'(B);
            3'b010: alu_out = 16'(A) & 16'(B);
            3'b011: alu_out = 16'(A) ^ 16'(B);
            3'b100: alu_out = A * B;
        default: alu_out = 'x;
        endcase
    end

    always_ff @(posedge clk)
        if (!reset_n)
            tmp_res <= '0;
        else if (state == READY && start)
            tmp_res <= alu_out;

    always_comb begin
        case (state)
            READY: begin
                done   = '0;
                result = 'x;
            end
            WAIT: begin
                done   = '0;
                result = 'x;
            end
            OUTPUT: begin
                done   = 1'b1;
                result = tmp_res;
            end
        endcase
    end

endmodule

