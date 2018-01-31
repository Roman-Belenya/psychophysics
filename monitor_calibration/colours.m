red = importdata('.spectra_data\red.dat');
green = importdata('.spectra_data\green.dat');
blue = importdata('.spectra_data\blue.dat');
lum = importdata('.spectra_data\luminance.dat');

x = linspace(0, 255, 32)';
k = lum.data(:,2);
r = red.data(:,2);
g = green.data(:,2);
b = blue.data(:,2);

m = zeros(4, 6);

[res, gof] = gammaFit(x, k);
m(1,:) = [min(k) max(k) res.gamma res.a res.b res.k];
plot(x, k, 'k.')
hold on
plot(x, gammaFcn(x, res), 'k-')

[res, gof] = gammaFit(x, r);
m(2,:) = [min(r) max(r) res.gamma res.a res.b res.k];
plot(x, r, 'r.')
hold on
plot(x, gammaFcn(x, res), 'r-')

[res, gof] = gammaFit(x, g);
m(3,:) = [min(g) max(g) res.gamma res.a res.b res.k];
plot(x, g, 'g.')
hold on
plot(x, gammaFcn(x, res), 'g-')

[res, gof] = gammaFit(x, b);
m(4,:) = [min(b) max(b) res.gamma res.a res.b res.k];
plot(x, b, 'b.')
hold on
plot(x, gammaFcn(x, res), 'b-')

