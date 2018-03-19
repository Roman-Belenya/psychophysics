g = importdata('.\calib_data\g_after.dat');
r = importdata('.\calib_data\r_after.dat');
levels = linspace(0, 255, 16);

plot(levels, r.data(:,2), 'r.', 'MarkerSize', 10)
hold on
plot(levels, g.data(:,2), 'g.', 'MarkerSize', 10)

grid on
xlim([-17 255+17])
set(gca, 'xtick', linspace(0, 255, 6))
set(gca, 'xticklabel', linspace(0, 255, 6))
xlabel('Input levels')
ylim([-10, max(g.data(:,2)+10)])
ylabel('Luminance')

coefs_red = polyfit(levels', r.data(:,2), 1);
lum_red = polyval(coefs_red, 225);

coefs_green = polyfit(levels', g.data(:,2), 1);
level_green = (lum_red - coefs_green(2)) / coefs_green(1);

plot(levels, polyval(coefs_red, levels), 'r-')
plot(levels, polyval(coefs_green, levels), 'g-')