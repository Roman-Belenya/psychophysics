function lum = gammaIFcn3(x, model)
    
    lum = model.a + (1 - x) .* (model.b .^ model.gamma) + x .* (model.b + model.k) .^ model.gamma;
end
