
%% Get data

delimeterIn = '\t';
headerlinesIn = 33;
spectra.bef = importdata('./calib/spectrum.dat', delimeterIn, headerlinesIn);
spectra.aft = importdata('./calib/spectrum_after.dat', delimeterIn, headerlinesIn);

l.bef = importdata('./calib/l.dat');
l.aft = importdata('./calib/l_after.dat');

r.bef = importdata('./calib/r.dat');
r.aft = importdata('./calib/r_after.dat');

g.bef = importdata('./calib/g.dat');
g.aft = importdata('./calib/g_after.dat');

b.bef = importdata('./calib/b.dat');
b.aft = importdata('./calib/b_after.dat');


%% Models


%% Spectrum plots

wv = spectra.bef.data(:, 1);

figure
plot(wv, spectra.bef.data(:, 2), 'r:')
hold on
plot(wv, spectra.aft.data(:, 2), 'r-')
plot(wv, spectra.bef.data(:, 3), 'g:')
plot(wv, spectra.aft.data(:, 3), 'g-')
plot(wv, spectra.bef.data(:, 4), 'b:')
plot(wv, spectra.aft.data(:, 4), 'b-')
xlabel('Wavelength (nm)')
ylabel('Radiance')


%% CIE plots

xs = [r.bef.data(end,4) g.bef.data(end,4) b.bef.data(end,4)];
ys = [r.bef.data(end,5) g.bef.data(end,5) b.bef.data(end,5)];

figure
cieplot()
hold on
plot(0.33, 0.33, 'wo')
plot([xs xs(1)], [ys ys(1)], 'ko-')

plot(r.bef.data(:,4), r.bef.data(:,5), 'w.-')
plot(g.bef.data(:,4), g.bef.data(:,5), 'w.-')
plot(b.bef.data(:,4), b.bef.data(:,5), 'w.-')
title('Before')

%%%
xs = [r.bef.data(end,4) g.bef.data(end,4) b.bef.data(end,4)];
ys = [r.bef.data(end,5) g.bef.data(end,5) b.bef.data(end,5)];

figure
cieplot()
hold on
plot(0.33, 0.33, 'wo')
plot([xs xs(1)], [ys ys(1)], 'ko-')

plot(r.aft.data(:,4), r.aft.data(:,5), 'w.-')
plot(g.aft.data(:,4), g.aft.data(:,5), 'w.-')
plot(b.aft.data(:,4), b.aft.data(:,5), 'w.-')
title('After')


