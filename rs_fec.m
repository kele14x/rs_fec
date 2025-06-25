%%
clc;
clearvars;
close all;

m = 8; % Number of bits per symbol
n = 2^m - 1; % Codeword length
t = 2;
k = n - t * 2;
s = 187;
prim_poly = 285;
B = 1;
[genpoly, t] = rsgenpoly(n, k, prim_poly, B);

%%
msg = gf(randi(n, 1, k-s), m);

code = rsenc(msg, n-s, k-s, genpoly);

decoded = rsdec(code, n-s, k-s, genpoly);

if all(msg == decoded)
    fprintf("Decode correct\n");
else
    fprintf("Decode with error\n");
end

% %% Gen Poly
% alpha = gf(2, m, prim_poly);
%
% x = alpha .^ (B+(0:15));
% y = gf(ones(1, 17), m, prim_poly);
%
% for i = 1:16
%     C = gf(nchoosek(x.x, i), m, prim_poly);
%
%     % Prod of all columns
%     t0 = gf(ones(size(C, 1), 1), m, prim_poly);
%     for col = 1:size(C, 2)
%         t0 = t0 .* C(:, col);
%     end
%
%     % Sum of all rows
%     t1 = gf(0, m, prim_poly);
%     for row = 1:size(t0, 1)
%         t1 = t1 + t0(row);
%     end
%
%     y(i+1) = t1;
% end
% assert(all(y == genpoly));
