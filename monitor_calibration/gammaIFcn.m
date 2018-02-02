function x = gammaIFcn(Lum, params)
    p1 = (1 - Lum).*params.b^params.gamma;
    p2 = Lum.*(params.b+params.k)^params.gamma;
    p3 = (p1 + p2).^(1/params.gamma) - params.b;
    x = p3./params.k;
end