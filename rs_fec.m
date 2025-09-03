%%
clc;
clearvars;
close all;

%%
p = 2;
m = 8;
t = 2;
s = 187;
b = 0;
prim_poly = 285;
ber = 0.02;

n = p^m - 1;
k = n - 2 * t;
genpoly = rsgenpoly(n, k, prim_poly, b);

length = 100000;

msg = gf(randi(n, [length, k - s]), m);
encoded = rsenc(msg, n-s, k-s, genpoly);

error = gf(randi(n, size(encoded)), m);
loc_error = rand(size(encoded)) < (1 - ber);
error(loc_error) = 0;
n_error = sum(error.x > 0, 2);

code = encoded + error;

[~, cnumerr, ccode] = rsdec(code, n-s, k-s, genpoly);

writematrix(code.x, "code.csv");
writematrix(cnumerr, "cnumerr.csv");
writematrix(ccode.x, "ccode.csv");
