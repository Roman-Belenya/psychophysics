spectrum = importdata('./spectra_data/spectra.csv');
red = importdata('./spectra_data/red.dat');
green = importdata('./spectra_data/green.dat');
blue = importdata('./spectra_data/blue.dat');

wv = spectrum.data(:, 1);

figure
plot(wv, spectrum.data(:, 2), 'r-')
hold on
plot(wv, spectrum.data(:, 3), 'g-')
plot(wv, spectrum.data(:, 4), 'b-')
xlabel('Wavelength (nm)')
ylabel('Radiance')


xs = [0.6466 0.2216 0.1526];
ys = [0.3311 0.6643 0.0812];
figure
cieplot()
hold on
plot(0.33, 0.33, 'wo')
plot([xs xs(1)], [ys ys(1)], 'ko-')

plot(red.data(:,4), red.data(:,5), 'w.-')
plot(green.data(:,4), green.data(:,5), 'w.-')
plot(blue.data(:,4), blue.data(:,5), 'w.-')