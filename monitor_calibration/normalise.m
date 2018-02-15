function y = normalise(x)
    y = (x - min(x)) ./ (max(x) - min(x));
end