red = importdata('./spectra_data/red.dat');
green = importdata('./spectra_data/green.dat');
blue = importdata('./spectra_data/blue.dat');
lum = importdata('./spectra_data/luminance.dat');

x = linspace(0, 255, 32)';
L = [lum.data(:,2) red.data(:,2) green.data(:,2) blue.data(:,2)];
m = zeros(4, 6);
c = ['k' 'r' 'g' 'b'];

figure
for i = 1:4
    subplot(2,2,i)
    [res, gof] = gammaFit(x, L(:,i));
    m(i,:) = [min(L(:,i)) max(L(:,i)) res.gamma res.a res.b res.k];
    

    plot(x, L(:,i), strcat(c(i), '.'))
    hold on
    plot(x, gammaFcn(x, res), c(i))
    plot(x, gammaIFcn2(x, res), c(i))
    plot(x, gammaIFcn2(gammaFcn(x, res), res), c(i))
end

% subplot(2,2,2)
% [res, gof] = gammaFit(x, r);
% m(2,:) = [min(r) max(r) res.gamma res.a res.b res.k];
% plot(x, r, 'r.')
% hold on
% plot(x, gammaFcn(x, res), 'r-')
% plot(x, gammaIFcn2(x, res), 'r-')
% plot(x, gammaIFcn2(gammaFcn(x, res), res), 'rx')
% 
% subplot(2,2,3)
% [res, gof] = gammaFit(x, g);
% m(3,:) = [min(g) max(g) res.gamma res.a res.b res.k];
% plot(x, g, 'g.')
% hold on
% plot(x, gammaFcn(x, res), 'g-')
% plot(x, gammaIFcn2(x, res), 'g-')
% plot(x, gammaIFcn2(gammaFcn(x, res), res), 'gx')
% 
% subplot(2,2,4)
% [res, gof] = gammaFit(x, b);
% m(4,:) = [min(b) max(b) res.gamma res.a res.b res.k];
% plot(x, b, 'b.')
% hold on
% plot(x, gammaFcn(x, res), 'b-')
% plot(x, gammaIFcn2(x, res), 'b-')
% plot(x, gammaIFcn2(gammaFcn(x, res), res), 'bx')


