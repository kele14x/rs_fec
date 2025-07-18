`timescale 1 ns / 1 ps
//
`default_nettype none

module bch_encoder (
    input  wire         clk,
    input  wire         rst_n,
    //
    input  wire [511:0] data_in,
    input  wire         vld_in,
    //
    output wire [511:0] data_out,
    output wire [ 19:0] parity_out,
    output wire         vld_out
);

  logic [511:0] data_in_reg;
  logic         vld_in_reg;

  logic [511:0] data_out_reg;
  logic         vld_out_reg;

  logic [ 19:0] parity;

  localparam [511:0] h_table[20] = {
    512'ha10afb3379c84706acaec62acef0ad24dddb57a202e0a4bda9c1e027dd0d6beab71ea604219c225a294cdf9719c829e7ffedf98b9162f68164e06dda9f18c301,
    512'he31f0d558a58c90bf5f34a7f5311f76d666df8e60721edc6fa4220686717bc3fd923ea0c62a466ee7bd560b92a587a2800360a9cb3a71b83ad20b66fa1294503,
    512'h6734e1986d79d511474852d468d343fe1100a66e0ca37f305d45a0f7132213950559721ce4d4ef86dee61ee54d78ddb7ff81ecb2f62cc1863ea10105dd4a4907,
    512'hce69c330daf3aa228e90a5a8d1a687fc22014cdc1946fe60ba8b41ee2644272a0ab2e439c9a9df0dbdcc3dca9af1bb6fff03d965ec59830c7d42020bba94920e,
    512'h3dd97d52cc2f1343b18f8d7b6dbda2dc99d9ce1a306d587cdcd763fb918525bea27b6e77b2cf9c4152d4a4022c2b5f3801ea4b4049d1f0999e6469cdea31e71d,
    512'hdab80196e1966181cfb1dcdc158be89dee68cb96623a1444106f27d0fe072097f3e87aeb44031ad88ce59793419e9797fc396f0b02c117b25828be414b7b0d3b,
    512'h147af81ebae4840533cd7f92e5e77c1f010ac08ec6948c35891faf8621032ac550ce53d2a99a17eb3087f0b19af506c8079f279d94e0d9e5d4b1115809eed977,
    512'h28f5f03d75c9080a679aff25cbcef83e0215811d8d29186b123f5f0c4206558aa19ca7a553342fd6610fe16335ea0d900f3e4f3b29c1b3cba96222b013ddb2ee,
    512'h51ebe07aeb921014cf35fe4b979df07c042b023b1a5230d6247ebe18840cab1543394f4aa6685facc21fc2c66bd41b201e7c9e765383679752c4456027bb65dc,
    512'ha3d7c0f5d72420299e6bfc972f3be0f80856047634a461ac48fd7c310819562a86729e954cd0bf59843f858cd7a836403cf93ceca706cf2ea5888ac04f76cbb8,
    512'h47af81ebae4840533cd7f92e5e77c1f010ac08ec6948c35891faf8621032ac550ce53d2a99a17eb3087f0b19af506c8079f279d94e0d9e5d4b1115809eed9770,
    512'h2e55f8e42558c7a0d5013476721f2ec4fc83467ad071220c8a3410e3fd683340aed4dc5112dedf3c39b2c9a44768f0e70c090a390d79ca3bf2c246dba2c3ede1,
    512'hfda10afb3379c84706acaec62acef0ad24dddb57a202e0a4bda9c1e027dd0d6beab71ea604219c225a294cdf9719c829e7ffedf98b9162f68164e06dda9f18c3,
    512'hfb4215f666f3908e0d595d8c559de15a49bbb6af4405c1497b5383c04fba1ad7d56e3d4c08433844b45299bf2e339053cfffdbf31722c5ed02c9c0dbb53e3186,
    512'hf6842beccde7211c1ab2bb18ab3bc2b493776d5e880b8292f6a707809f7435afaadc7a981086708968a5337e5c6720a79fffb7e62e458bda059381b76a7c630c,
    512'hed0857d99bce4238356576315677856926eedabd10170525ed4e0f013ee86b5f55b8f530210ce112d14a66fcb8ce414f3fff6fcc5c8b17b40b27036ed4f8c618,
    512'hda10afb3379c84706acaec62acef0ad24dddb57a202e0a4bda9c1e027dd0d6beab71ea604219c225a294cdf9719c829e7ffedf98b9162f68164e06dda9f18c30,
    512'hb4215f666f3908e0d595d8c559de15a49bbb6af4405c1497b5383c04fba1ad7d56e3d4c08433844b45299bf2e339053cfffdbf31722c5ed02c9c0dbb53e31860,
    512'h6842beccde7211c1ab2bb18ab3bc2b493776d5e880b8292f6a707809f7435afaadc7a981086708968a5337e5c6720a79fffb7e62e458bda059381b76a7c630c0,
    512'hd0857d99bce4238356576315677856926eedabd10170525ed4e0f013ee86b5f55b8f530210ce112d14a66fcb8ce414f3fff6fcc5c8b17b40b27036ed4f8c6180
  };

  always @(posedge clk) begin
    if (!rst_n) begin
      data_in_reg <= 512'b0;
      vld_in_reg  <= 1'b0;
    end else begin
      data_in_reg <= data_in;
      vld_in_reg  <= vld_in;
    end
  end

  always @(posedge clk) begin
    if (!rst_n) begin
      data_out_reg <= 512'b0;
      vld_out_reg  <= 1'b0;
    end else begin
      data_out_reg <= data_in_reg;  // Pass through data
      vld_out_reg  <= vld_in_reg;  // Pass through valid signal
    end
  end

  always @(posedge clk) begin : p_code
    integer i;
    if (!rst_n) begin
      parity <= 0;
    end else begin
      for (i = 0; i < 20; i = i + 1) begin
        parity[i] <= ^(data_in_reg & h_table[i]);
      end
    end
  end

  assign data_out   = data_out_reg;
  assign parity_out = parity;
  assign vld_out    = vld_out_reg;

endmodule

`default_nettype wire
// End of bch_encoder.v
