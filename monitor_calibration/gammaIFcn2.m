function x = gammaIFcn2(Lum, params)
    Lum(Lum >= params.a) = ((Lum(Lum >= params.a) - params.a).^(1/params.gamma) - params.b) ./ params.k;
    Lum(Lum < params.a) = -params.b/params.k;
    x = Lum;
end
