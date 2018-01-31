function Lum = gammaFcn(x, params)
    Lum = params.a + (params.b + params.k .* x) .^ params.gamma;
end
