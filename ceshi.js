ci = function (t) {
    function r() {
        var e = null !== t && t.apply(this, arguments) || this;
        return e.tag = "[HttpStatsClick]",
            e.url = "//api.bilibili.com/x/click-interface/click/web/h5",
            e
    }

    return (0, e.ZT)(r, t), r.prototype.r = function (t) {
        return (0, e.mG)(this, void 0, void 0, (function () {
                return (0, e.Jh)(this, (function (e) {
                        return [2, this.request({
                            url: this.url,
                            method: "POST",
                            data: t,
                            withCredentials: !0
                        })]
                    }
                ))
            }
        ))
    },
        r
}(ut.e)