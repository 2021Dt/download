function createCommonjsModule(e, t) {
        return e(t = {
            exports: {}
        }, t.exports),
        t.exports
    }
var crypt = createCommonjsModule((function(e) {
        var t, r;
        t = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
        r = {
            rotl: function(e, t) {
                return e << t | e >>> 32 - t
            },
            rotr: function(e, t) {
                return e << 32 - t | e >>> t
            },
            endian: function(e) {
                if (e.constructor == Number)
                    return 16711935 & r.rotl(e, 8) | 4278255360 & r.rotl(e, 24);
                for (var t = 0; t < e.length; t++)
                    e[t] = r.endian(e[t]);
                return e
            },
            randomBytes: function(e) {
                for (var t = []; e > 0; e--)
                    t.push(Math.floor(256 * Math.random()));
                return t
            },
            bytesToWords: function(e) {
                for (var t = [], r = 0, n = 0; r < e.length; r++,
                n += 8)
                    t[n >>> 5] |= e[r] << 24 - n % 32;
                return t
            },
            wordsToBytes: function(e) {
                for (var t = [], r = 0; r < 32 * e.length; r += 8)
                    t.push(e[r >>> 5] >>> 24 - r % 32 & 255);
                return t
            },
            bytesToHex: function(e) {
                for (var t = [], r = 0; r < e.length; r++)
                    t.push((e[r] >>> 4).toString(16)),
                    t.push((15 & e[r]).toString(16));
                return t.join("")
            },
            hexToBytes: function(e) {
                for (var t = [], r = 0; r < e.length; r += 2)
                    t.push(parseInt(e.substr(r, 2), 16));
                return t
            },
            bytesToBase64: function(e) {
                for (var r = [], n = 0; n < e.length; n += 3)
                    for (var o = e[n] << 16 | e[n + 1] << 8 | e[n + 2], i = 0; i < 4; i++)
                        8 * n + 6 * i <= 8 * e.length ? r.push(t.charAt(o >>> 6 * (3 - i) & 63)) : r.push("=");
                return r.join("")
            },
            base64ToBytes: function(e) {
                e = e.replace(/[^A-Z0-9+\/]/gi, "");
                for (var r = [], n = 0, o = 0; n < e.length; o = ++n % 4)
                    0 != o && r.push((t.indexOf(e.charAt(n - 1)) & Math.pow(2, -2 * o + 8) - 1) << 2 * o | t.indexOf(e.charAt(n)) >>> 6 - 2 * o);
                return r
            }
        },
        e.exports = r
    }
    ))
      , charenc = {
        utf8: {
            stringToBytes: function(e) {
                return charenc.bin.stringToBytes(unescape(encodeURIComponent(e)))
            },
            bytesToString: function(e) {
                return decodeURIComponent(escape(charenc.bin.bytesToString(e)))
            }
        },
        bin: {
            stringToBytes: function(e) {
                for (var t = [], r = 0; r < e.length; r++)
                    t.push(255 & e.charCodeAt(r));
                return t
            },
            bytesToString: function(e) {
                for (var t = [], r = 0; r < e.length; r++)
                    t.push(String.fromCharCode(e[r]));
                return t.join("")
            }
        }
    }
      , charenc_1 = charenc
      , isBuffer_1 = function(e) {
        return null != e && (isBuffer(e) || isSlowBuffer(e) || !!e._isBuffer)
    };
    function isBuffer(e) {
        return !!e.constructor && "function" == typeof e.constructor.isBuffer && e.constructor.isBuffer(e)
    }
    function isSlowBuffer(e) {
        return "function" == typeof e.readFloatLE && "function" == typeof e.slice && isBuffer(e.slice(0, 0))
    }

    var md5 = createCommonjsModule((function(e) {
        var t, r, n, o, i;
        t = crypt,
        r = charenc_1.utf8,
        n = isBuffer_1,
        o = charenc_1.bin,
        (i = function e(i, a) {
            i.constructor == String ? i = a && "binary" === a.encoding ? o.stringToBytes(i) : r.stringToBytes(i) : n(i) ? i = Array.prototype.slice.call(i, 0) : Array.isArray(i) || i.constructor === Uint8Array || (i = i.toString());
            for (var s = t.bytesToWords(i), l = 8 * i.length, c = 1732584193, u = -271733879, d = -1732584194, p = 271733878, h = 0; h < s.length; h++)
                s[h] = 16711935 & (s[h] << 8 | s[h] >>> 24) | 4278255360 & (s[h] << 24 | s[h] >>> 8);
            s[l >>> 5] |= 128 << l % 32,
            s[14 + (l + 64 >>> 9 << 4)] = l;
            var f = e._ff
              , m = e._gg
              , v = e._hh
              , g = e._ii;
            for (h = 0; h < s.length; h += 16) {
                var y = c
                  , _ = u
                  , $ = d
                  , b = p;
                c = f(c, u, d, p, s[h + 0], 7, -680876936),
                p = f(p, c, u, d, s[h + 1], 12, -389564586),
                d = f(d, p, c, u, s[h + 2], 17, 606105819),
                u = f(u, d, p, c, s[h + 3], 22, -1044525330),
                c = f(c, u, d, p, s[h + 4], 7, -176418897),
                p = f(p, c, u, d, s[h + 5], 12, 1200080426),
                d = f(d, p, c, u, s[h + 6], 17, -1473231341),
                u = f(u, d, p, c, s[h + 7], 22, -45705983),
                c = f(c, u, d, p, s[h + 8], 7, 1770035416),
                p = f(p, c, u, d, s[h + 9], 12, -1958414417),
                d = f(d, p, c, u, s[h + 10], 17, -42063),
                u = f(u, d, p, c, s[h + 11], 22, -1990404162),
                c = f(c, u, d, p, s[h + 12], 7, 1804603682),
                p = f(p, c, u, d, s[h + 13], 12, -40341101),
                d = f(d, p, c, u, s[h + 14], 17, -1502002290),
                c = m(c, u = f(u, d, p, c, s[h + 15], 22, 1236535329), d, p, s[h + 1], 5, -165796510),
                p = m(p, c, u, d, s[h + 6], 9, -1069501632),
                d = m(d, p, c, u, s[h + 11], 14, 643717713),
                u = m(u, d, p, c, s[h + 0], 20, -373897302),
                c = m(c, u, d, p, s[h + 5], 5, -701558691),
                p = m(p, c, u, d, s[h + 10], 9, 38016083),
                d = m(d, p, c, u, s[h + 15], 14, -660478335),
                u = m(u, d, p, c, s[h + 4], 20, -405537848),
                c = m(c, u, d, p, s[h + 9], 5, 568446438),
                p = m(p, c, u, d, s[h + 14], 9, -1019803690),
                d = m(d, p, c, u, s[h + 3], 14, -187363961),
                u = m(u, d, p, c, s[h + 8], 20, 1163531501),
                c = m(c, u, d, p, s[h + 13], 5, -1444681467),
                p = m(p, c, u, d, s[h + 2], 9, -51403784),
                d = m(d, p, c, u, s[h + 7], 14, 1735328473),
                c = v(c, u = m(u, d, p, c, s[h + 12], 20, -1926607734), d, p, s[h + 5], 4, -378558),
                p = v(p, c, u, d, s[h + 8], 11, -2022574463),
                d = v(d, p, c, u, s[h + 11], 16, 1839030562),
                u = v(u, d, p, c, s[h + 14], 23, -35309556),
                c = v(c, u, d, p, s[h + 1], 4, -1530992060),
                p = v(p, c, u, d, s[h + 4], 11, 1272893353),
                d = v(d, p, c, u, s[h + 7], 16, -155497632),
                u = v(u, d, p, c, s[h + 10], 23, -1094730640),
                c = v(c, u, d, p, s[h + 13], 4, 681279174),
                p = v(p, c, u, d, s[h + 0], 11, -358537222),
                d = v(d, p, c, u, s[h + 3], 16, -722521979),
                u = v(u, d, p, c, s[h + 6], 23, 76029189),
                c = v(c, u, d, p, s[h + 9], 4, -640364487),
                p = v(p, c, u, d, s[h + 12], 11, -421815835),
                d = v(d, p, c, u, s[h + 15], 16, 530742520),
                c = g(c, u = v(u, d, p, c, s[h + 2], 23, -995338651), d, p, s[h + 0], 6, -198630844),
                p = g(p, c, u, d, s[h + 7], 10, 1126891415),
                d = g(d, p, c, u, s[h + 14], 15, -1416354905),
                u = g(u, d, p, c, s[h + 5], 21, -57434055),
                c = g(c, u, d, p, s[h + 12], 6, 1700485571),
                p = g(p, c, u, d, s[h + 3], 10, -1894986606),
                d = g(d, p, c, u, s[h + 10], 15, -1051523),
                u = g(u, d, p, c, s[h + 1], 21, -2054922799),
                c = g(c, u, d, p, s[h + 8], 6, 1873313359),
                p = g(p, c, u, d, s[h + 15], 10, -30611744),
                d = g(d, p, c, u, s[h + 6], 15, -1560198380),
                u = g(u, d, p, c, s[h + 13], 21, 1309151649),
                c = g(c, u, d, p, s[h + 4], 6, -145523070),
                p = g(p, c, u, d, s[h + 11], 10, -1120210379),
                d = g(d, p, c, u, s[h + 2], 15, 718787259),
                u = g(u, d, p, c, s[h + 9], 21, -343485551),
                c = c + y >>> 0,
                u = u + _ >>> 0,
                d = d + $ >>> 0,
                p = p + b >>> 0
            }
            return t.endian([c, u, d, p])
        }
        )._ff = function(e, t, r, n, o, i, a) {
            var s = e + (t & r | ~t & n) + (o >>> 0) + a;
            return (s << i | s >>> 32 - i) + t
        }
        ,
        i._gg = function(e, t, r, n, o, i, a) {
            var s = e + (t & n | r & ~n) + (o >>> 0) + a;
            return (s << i | s >>> 32 - i) + t
        }
        ,
        i._hh = function(e, t, r, n, o, i, a) {
            var s = e + (t ^ r ^ n) + (o >>> 0) + a;
            return (s << i | s >>> 32 - i) + t
        }
        ,
        i._ii = function(e, t, r, n, o, i, a) {
            var s = e + (r ^ (t | ~n)) + (o >>> 0) + a;
            return (s << i | s >>> 32 - i) + t
        }
        ,
        i._blocksize = 16,
        i._digestsize = 16,
        e.exports = function(e, r) {
            if (null == e)
                throw new Error("Illegal argument " + e);
            var n = t.wordsToBytes(i(e, r));
            return r && r.asBytes ? n : r && r.asString ? o.bytesToString(n) : t.bytesToHex(n)
        }
    }
    ));


function getMixinKey(e) {
        var t = [];
        return [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52].forEach((function(r) {
            e.charAt(r) && t.push(e.charAt(r))
        }
        )),
        t.join("").slice(0, 32)
    };


function wordsToBytes(e) {
    for (var t = [], r = 0; r < 32 * e.length; r += 8)
        t.push(e[r >>> 5] >>> 24 - r % 32 & 255);
    return t
}

function wts(){
    return Math.round(Date.now() / 1e3).toString();
}


function w_rid(q){
    var o = ans = getMixinKey('7cd084941338484aae1ad9425b84077c4932caff0ff746eab6f01bf08b70ac45');
    var ans = wordsToBytes(q + o);
    return md5(q + o);
}
