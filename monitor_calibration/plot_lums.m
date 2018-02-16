function [fig, ax] = plot_lums(levels, before, after, col)

    [res, gof] = gammaFit(levels, before);
    fit_line = gammaFcn(levels, res);

    h1 = plot(levels, after, '.', 'Color', col, 'markersize', 10);
    hold on
    h2 = lsline();
    h3 = plot(levels, before, 'o', 'Color', col);
    h4= plot(levels, fit_line, '-', 'Color', col);

    xlim([-5 260])
    set(h2, 'LineStyle', ':');
    xlabel('Input')
    ylabel('Luminance (cd/m^2)')
    legend([h3, h1, h4], {'measurement before', 'measurement after',...
        'gamma model'}, 'location', 'northwest')
    
    fig = gcf;
    ax = gca;
end