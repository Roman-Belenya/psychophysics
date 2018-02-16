
%% Get data

delimeterIn = '\t';
headerlinesIn = 33;

spectrum = importdata('./calib_data/spectra/rgb.dat', delimeterIn, headerlinesIn);

l.bef = importdata('./calib_data/l.dat');
l.aft = importdata('./calib_data/l_after.dat');

r.bef = importdata('./calib_data/r.dat');
r.aft = importdata('./calib_data/r_after.dat');

g.bef = importdata('./calib_data/g.dat');
g.aft = importdata('./calib_data/g_after.dat');

b.bef = importdata('./calib_data/b.dat');
b.aft = importdata('./calib_data/b_after.dat');


%% Models

levels = linspace(0, 255, 16)';

figure()
subplot(2,2,1)
plot_lums(levels, l.bef.data(:, 2), l.aft.data(:, 2), 'k')

subplot(2,2,2)
plot_lums(levels, r.bef.data(:, 2), r.aft.data(:, 2), [0.6350 0.0780 0.1840])

subplot(2,2,3)
plot_lums(levels, g.bef.data(:, 2), g.aft.data(:, 2), [0.4660 0.6740 0.1880])

subplot(2,2,4)
plot_lums(levels, b.bef.data(:, 2), b.aft.data(:, 2), [0 0.4470 0.7410])

% tbl = table(levels, l.aft.data(:,2), 'VariableNames', {'levels', 'lums'});
% mdl = fitlm(tbl, 'lums~levels');
% plot(mdl)



%% Spectrum plots

wv = spectrum.data(:, 1);

figure
plot(wv, spectrum.data(:, 2), 'r-')
hold on
plot(wv, spectrum.data(:, 3), 'g-')
plot(wv, spectrum.data(:, 4), 'b-')
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


