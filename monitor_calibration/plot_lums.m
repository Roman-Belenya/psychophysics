function [fig, ax] = plot_lums(levels, before, after, col)

    [res, gof] = gammaFit(levels, before);
    gamma_fit = gammaFcn(levels, res);
    lin_fit = polyfit(levels, after, 1);

    h1 = plot(levels, after, '.', 'Color', col, 'markersize', 10);
    hold on
    h2 = plot(levels, polyval(lin_fit, levels), ':', 'Color', col);
    h3 = plot(levels, before, 'o', 'Color', col);
    h4 = plot(levels, gamma_fit, '-', 'Color', col);

    xlim([-5 260])
    set(h2, 'LineStyle', ':');
    xlabel('Input')
    ylabel('Luminance (cd/m^2)')
    legend([h3, h1, h4], {'measurement before', 'measurement after',...
        sprintf('%s = %1.2f', '\gamma', res.gamma)}, 'location', 'northwest')
    
    fig = gcf;
    ax = gca;
end