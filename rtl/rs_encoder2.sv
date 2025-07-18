`timescale 1 ns / 1 ps
//
`default_nettype none

module rs_encoder (
    input  wire       clk,
    input  wire       rst_n,
    //
    input  wire [7:0] msg_in    [64],
    input  wire       vld_in,
    //
    output wire [7:0] msg_out   [64],
    output wire [7:0] parity_out[ 4],
    output wire       vld_out
);

  localparam logic [7:0] prim = 8'h1d;

  // verilog_format: off
  localparam logic [7:0] g_table [64][4] = '{
    {241,  12, 191,  74},
    { 12, 121, 197, 111},
    { 10, 192,  90, 125},
    {243,  90, 186, 136},
    {182,  22, 187,  75},
    {229,  95, 135, 215},
    {230,  46, 187, 223},
    {253,   2,  48, 106},
    { 96, 201,   4, 254},
    {120,  89,  64, 119},
    { 39, 197, 105, 126},
    {213, 212,  87,  98},
    {123, 206,  40,  16},
    { 54,  37,  39,  39},
    {201, 176, 127,  42},
    {184, 152,  53, 141},
    {220, 165,  92, 178},
    { 56,  54,  40,  80},
    {238,   3,  92,  27},
    { 11,  60, 248,   3},
    { 38, 168, 212,  33},
    {133, 251,  63, 118},
    {206,  89, 147, 189},
    {134,  49, 187,   5},
    {106, 126,  20, 205},
    {  4,  18,  57, 175},
    {127, 103, 169, 197},
    { 31,  40, 218, 155},
    {166,   7, 200, 253},
    { 94,  60, 102,  98},
    {123,  69, 192,  33},
    {133, 166, 210,  98},
    {123, 158,  90, 149},
    {241,  23,  73,  91},
    {211,  70, 111,  42},
    {184, 130, 195, 157},
    {234, 251, 175,  75},
    {229,   3, 106, 195},
    { 83, 233, 115, 247},
    {138,  36, 194,  53},
    { 48, 144,  39, 165},
    {171, 190,  97,  55},
    {255, 115,  13,  99},
    {146, 133, 215, 246},
    { 99, 132, 246,  45},
    { 29,   8, 148,  23},
    {147, 121, 116, 136},
    {182, 118, 152, 133},
    {199, 132,  72, 150},
    {215,   8, 187, 144},
    {155,  67, 250, 204},
    {237, 130,  92, 253},
    { 94, 119, 227, 246},
    { 99,  72,   4,  25},
    {196, 115,   3,  62},
    { 13,  82,  98,  52},
    {217, 118,   9, 185},
    {  5, 191, 233,  85},
    {132, 198, 240, 172},
    { 89,  68, 149, 213},
    { 41,  80,  16, 168},
    {218, 112, 126, 255},
    {145, 130, 161, 177},
    { 30, 216, 231, 116}
  };
  // verilog_format: on

  logic [7:0] msg_reg [64];
  logic       vld_reg;

  logic [7:0] msg_a0  [64];
  logic [7:0] msg_a1  [64];
  logic [7:0] msg_a2  [64];
  logic [7:0] msg_a3  [64];
  logic [7:0] msg_a4  [64];
  logic [7:0] msg_a5  [64];
  logic [7:0] msg_a6  [64];
  logic [7:0] msg_a7  [64];

  logic [7:0] mul     [64] [4];
  logic [7:0] add     [ 4];
  logic [7:0] msg_r2  [64];
  logic [7:0] parity  [ 4];
  logic       valid;

  // Input registers
  always_ff @(posedge clk) begin
    msg_reg <= msg_in;
    vld_reg <= vld_in;
  end

  generate
    for (genvar i = 0; i < 64; i++) begin : g_mul

      assign msg_a0[i] = msg_reg[i];
      assign msg_a1[i] = {msg_a0[i][6:0], 1'b0} ^ (msg_a0[i][7] ? prim : 8'b0);
      assign msg_a2[i] = {msg_a1[i][6:0], 1'b0} ^ (msg_a1[i][7] ? prim : 8'b0);
      assign msg_a3[i] = {msg_a2[i][6:0], 1'b0} ^ (msg_a2[i][7] ? prim : 8'b0);
      assign msg_a4[i] = {msg_a3[i][6:0], 1'b0} ^ (msg_a3[i][7] ? prim : 8'b0);
      assign msg_a5[i] = {msg_a4[i][6:0], 1'b0} ^ (msg_a4[i][7] ? prim : 8'b0);
      assign msg_a6[i] = {msg_a5[i][6:0], 1'b0} ^ (msg_a5[i][7] ? prim : 8'b0);
      assign msg_a7[i] = {msg_a6[i][6:0], 1'b0} ^ (msg_a6[i][7] ? prim : 8'b0);

      for (genvar j = 0; j < 4; j++) begin

        assign mul[i][j] =
          (g_table[i][j][0] ? msg_a0[i] : 8'b0) ^
          (g_table[i][j][1] ? msg_a1[i] : 8'b0) ^
          (g_table[i][j][2] ? msg_a2[i] : 8'b0) ^
          (g_table[i][j][3] ? msg_a3[i] : 8'b0) ^
          (g_table[i][j][4] ? msg_a4[i] : 8'b0) ^
          (g_table[i][j][5] ? msg_a5[i] : 8'b0) ^
          (g_table[i][j][6] ? msg_a6[i] : 8'b0) ^
          (g_table[i][j][7] ? msg_a7[i] : 8'b0);

      end
    end
  endgenerate

  generate
    for (genvar j = 0; j < 4; j++) begin : g_add

      always_comb begin
        add[j] = '0;
        for (int i = 0; i < 64; i++) begin
          add[j] = add[j] ^ mul[i][j];
        end
      end

    end
  endgenerate

  always_ff @(posedge clk) begin
    msg_r2 <= msg_reg;
  end

  assign msg_out = msg_r2;

  generate
    for (genvar j = 0; j < 4; j++) begin : g_parity

      always_ff @(posedge clk) begin
        parity[j] <= add[j];
      end

      assign parity_out[j] = parity[j];

    end
  endgenerate

  always_ff @(posedge clk) begin
    valid <= vld_reg;
  end

  assign vld_out = valid;

endmodule

`default_nettype wire
