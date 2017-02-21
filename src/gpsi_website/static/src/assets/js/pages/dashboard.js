$(function() {
    function t(t, e) {
        function a() {
            i = n.node().getBoundingClientRect().width - r.left - r.right, v.attr("width", i + r.left + r.right), x.attr("width", i + r.left + r.right), u.range([0, i]), x.selectAll(".d3-axis-horizontal").call(h), x.selectAll(".d3-axis-subticks").attr("x1", u).attr("x2", u), x.selectAll(".d3-grid-dashed").call(y.tickSize(-i, 0, 0)), x.selectAll(".d3-axis-right").attr("transform", "translate(" + i + ", 0)"), x.selectAll(".streamgraph-layer").attr("d", function(t) {
                return k(t.values)
            })
        }
        var n = d3.select(t),
            r = {
                top: 5,
                right: 50,
                bottom: 40,
                left: 50
            },
            i = n.node().getBoundingClientRect().width - r.left - r.right,
            e = e - r.top - r.bottom,
            s = 30,
            l = n.append("div").attr("class", "d3-tip e").style("display", "none"),
            o = d3.time.format("%m/%d/%y %H:%M"),
            d = d3.time.format("%H:%M"),
            c = ["#03A9F4", "#29B6F6", "#4FC3F7", "#81D4FA", "#B3E5FC", "#E1F5FE"],
            u = d3.time.scale().range([0, i]),
            p = d3.scale.linear().range([e, 0]),
            f = d3.scale.ordinal().range(c),
            h = d3.svg.axis().scale(u).orient("bottom").ticks(d3.time.hours, 4).innerTickSize(4).tickPadding(8).tickFormat(d3.time.format("%H:%M")),
            m = d3.svg.axis().scale(p).ticks(6).innerTickSize(4).outerTickSize(0).tickPadding(8).tickFormat(function(t) {
                return t / 1e3 + "k"
            }),
            g = m,
            y = d3.svg.axis().scale(p).orient("left").ticks(6).tickPadding(8).tickFormat("").tickSize(-i, 0, 0),
            v = n.append("svg"),
            x = v.attr("width", i + r.left + r.right).attr("height", e + r.top + r.bottom).append("g").attr("transform", "translate(" + r.left + "," + r.top + ")"),
            b = d3.layout.stack().offset("silhouette").values(function(t) {
                return t.values
            }).x(function(t) {
                return t.date
            }).y(function(t) {
                return t.value
            }),
            w = d3.nest().key(function(t) {
                return t.key
            }),
            k = d3.svg.area().interpolate("cardinal").x(function(t) {
                return u(t.date)
            }).y0(function(t) {
                return p(t.y0)
            }).y1(function(t) {
                return p(t.y0 + t.y)
            });
        d3.csv("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/traffic_sources.csv", function(a, c) {
            c.forEach(function(t) {
                t.date = o.parse(t.date), t.value = +t.value
            });
            var v = b(w.entries(c));
            u.domain(d3.extent(c, function(t, e) {
                return t.date
            })), p.domain([0, d3.max(c, function(t) {
                return t.y0 + t.y
            })]), x.append("g").attr("class", "d3-grid-dashed").call(y);
            var A = x.append("g").attr("class", "streamgraph-layers-group"),
                z = A.selectAll(".streamgraph-layer").data(v).enter().append("path").attr("class", "streamgraph-layer").attr("d", function(t) {
                    return k(t.values)
                }).style("stroke", "#fff").style("stroke-width", .5).style("fill", function(t, e) {
                    return f(e)
                }),
                C = z.style("opacity", 0).transition().duration(750).delay(function(t, e) {
                    return 50 * e
                }).style("opacity", 1);
            x.append("g").attr("class", "d3-axis d3-axis-left d3-axis-solid").call(m.orient("left")), d3.select(x.selectAll(".d3-axis-left .tick text")[0][0]).style("visibility", "hidden"), x.append("g").attr("class", "d3-axis d3-axis-right d3-axis-solid").attr("transform", "translate(" + i + ", 0)").call(g.orient("right")), d3.select(x.selectAll(".d3-axis-right .tick text")[0][0]).style("visibility", "hidden");
            var M = x.append("g").attr("class", "d3-axis d3-axis-horizontal d3-axis-solid").attr("transform", "translate(0," + e + ")").call(h);
            M.selectAll(".d3-axis-subticks").data(u.ticks(d3.time.hours), function(t) {
                return t
            }).enter().append("line").attr("class", "d3-axis-subticks").attr("y1", 0).attr("y2", 4).attr("x1", u).attr("x2", u);
            var B = A.append("g").attr("class", "hover-line"),
                F = B.append("line").attr("y1", 0).attr("y2", e).style("fill", "none").style("stroke", "#fff").style("stroke-width", 1).style("pointer-events", "none").style("shape-rendering", "crispEdges").style("opacity", 0),
                S = B.append("rect").attr("x", 2).attr("y", 2).attr("width", 6).attr("height", 6).style("fill", "#03A9F4").style("stroke", "#fff").style("stroke-width", 1).style("shape-rendering", "crispEdges").style("pointer-events", "none").style("opacity", 0);
            C.each("end", function() {
                z.on("mouseover", function(t, e) {
                    x.selectAll(".streamgraph-layer").transition().duration(250).style("opacity", function(t, a) {
                        return a != e ? .75 : 1
                    })
                }).on("mousemove", function(t, e) {
                    mouse = d3.mouse(this), mousex = mouse[0], mousey = mouse[1], datearray = [];
                    var a = u.invert(mousex);
                    a = a.getHours();
                    for (var n = t.values, r = 0; r < n.length; r++) datearray[r] = n[r].date, datearray[r] = datearray[r].getHours();
                    mousedate = datearray.indexOf(a), pro = t.values[mousedate].value, S.attr("x", mousex - 3).attr("y", mousey - 6).style("opacity", 1), F.attr("x1", mousex).attr("x2", mousex).style("opacity", 1), l.html("<ul class='list-unstyled mb-5'><li><div class='text-size-base mt-5 mb-5'><i class='icon-circle-left2 position-left'></i>" + t.key + "</div></li><li>Visits: &nbsp;<span class='text-semibold pull-right'>" + pro + "</span></li><li>Time: &nbsp; <span class='text-semibold pull-right'>" + d(t.values[mousedate].date) + "</span></li></ul>").style("display", "block"), l.append("div").attr("class", "d3-tip-arrow")
                }).on("mouseout", function(t, e) {
                    x.selectAll(".streamgraph-layer").transition().duration(250).style("opacity", 1), S.style("opacity", 0), l.style("display", "none"), F.style("opacity", 0)
                })
            }), n.on("mousemove", function(e, a) {
                mouse = d3.mouse(this), mousex = mouse[0], mousey = mouse[1], l.style("top", mousey - $(".d3-tip").outerHeight() / 2 - 2 + "px"), mousex >= $(t).outerWidth() - $(".d3-tip").outerWidth() - r.right - 2 * s ? l.style("left", mousex - $(".d3-tip").outerWidth() - s + "px").attr("class", "d3-tip w") : l.style("left", mousex + s + "px").attr("class", "d3-tip e")
            })
        }), $(window).on("resize", a), $(".sidebar-control").on("click", a)
    }

    function e(t, e) {
        function a() {
            d3.transition().duration(h ? 7500 : 500).each(n)
        }

        function n() {
            function t() {
                s = r.node().getBoundingClientRect().width - i.left - i.right, u.attr("width", s + i.left + i.right), p.attr("width", s + i.left + i.right), g.range([0, s]), y.range([e, 0]), p.select(".d3-axis-horizontal").call(v), p.select(".d3-axis-vertical").call(x.tickSize(0 - s)), p.selectAll(".d3-line").attr("d", function(t, e) {
                    return m(t.values)
                }), p.selectAll(".d3-line-circle").attr("cx", function(t, e) {
                    return g(t.date)
                })
            }
            var a = d3.nest().key(function(t) {
                    return t.type
                }).map(formatted),
                n = f.val(),
                d = a[n];
            c.domain(d3.keys(d[0]).filter(function(t) {
                return "date" !== t && "type" !== t
            }));
            var h = c.domain().map(function(t) {
                    return {
                        name: t,
                        values: d.map(function(e) {
                            return {
                                name: t,
                                date: o(e.date),
                                value: parseFloat(e[t], 10)
                            }
                        })
                    }
                }),
                m = d3.svg.line().x(function(t) {
                    return g(t.date)
                }).y(function(t) {
                    return y(t.value)
                }).interpolate("cardinal"),
                g = d3.time.scale().domain([d3.min(h, function(t) {
                    return d3.min(t.values, function(t) {
                        return t.date
                    })
                }), d3.max(h, function(t) {
                    return d3.max(t.values, function(t) {
                        return t.date
                    })
                })]).range([0, s]),
                y = d3.scale.linear().domain([d3.min(h, function(t) {
                    return d3.min(t.values, function(t) {
                        return t.value
                    })
                }), d3.max(h, function(t) {
                    return d3.max(t.values, function(t) {
                        return t.value
                    })
                })]).range([e, 0]),
                v = d3.svg.axis().scale(g).orient("bottom").tickPadding(8).ticks(d3.time.days).innerTickSize(4).tickFormat(d3.time.format("%a")),
                x = d3.svg.axis().scale(y).orient("left").ticks(6).tickSize(0 - s).tickPadding(8);
            p.append("g").attr("class", "d3-axis d3-axis-horizontal d3-axis-solid").attr("transform", "translate(0," + e + ")"), p.append("g").attr("class", "d3-axis d3-axis-vertical d3-axis-transparent");
            var b = p.selectAll(".lines").data(h),
                w = b.enter().append("g").attr("class", "lines").attr("id", function(t) {
                    return t.name + "-line"
                });
            w.append("path").attr("class", "d3-line d3-line-medium").style("stroke", function(t) {
                return c(t.name)
            }).style("opacity", 0).attr("d", function(t) {
                return m(t.values[0])
            }).transition().duration(500).delay(function(t, e) {
                return 200 * e
            }).style("opacity", 1);
            var k = b.selectAll("circle").data(function(t) {
                return t.values
            }).enter().append("circle").attr("class", "d3-line-circle d3-line-circle-medium").attr("cx", function(t, e) {
                return g(t.date)
            }).attr("cy", function(t, e) {
                return y(t.value)
            }).attr("r", 3).style("fill", "#fff").style("stroke", function(t) {
                return c(t.name)
            });
            k.style("opacity", 0).transition().duration(500).delay(500).style("opacity", 1), k.on("mouseover", function(t) {
                l.offset([-15, 0]).show(t), d3.select(this).transition().duration(250).attr("r", 4)
            }).on("mouseout", function(t) {
                l.hide(t), d3.select(this).transition().duration(250).attr("r", 3)
            }), b.each(function(t) {
                d3.select(d3.select(this).selectAll("circle")[0][0]).on("mouseover", function(t) {
                    l.offset([0, 15]).direction("e").show(t), d3.select(this).transition().duration(250).attr("r", 4)
                }).on("mouseout", function(t) {
                    l.direction("n").hide(t), d3.select(this).transition().duration(250).attr("r", 3)
                })
            }), b.each(function(t) {
                d3.select(d3.select(this).selectAll("circle")[0][d3.select(this).selectAll("circle").size() - 1]).on("mouseover", function(t) {
                    l.offset([0, -15]).direction("w").show(t), d3.select(this).transition().duration(250).attr("r", 4)
                }).on("mouseout", function(t) {
                    l.direction("n").hide(t), d3.select(this).transition().duration(250).attr("r", 3)
                })
            });
            var A = d3.transition(b);
            A.select("path").attr("d", function(t, e) {
                return m(t.values)
            }), A.selectAll("circle").attr("cy", function(t, e) {
                return y(t.value)
            }).attr("cx", function(t, e) {
                return g(t.date)
            }), d3.transition(p).select(".d3-axis-vertical").call(x), d3.transition(p).select(".d3-axis-horizontal").attr("transform", "translate(0," + e + ")").call(v), $(window).on("resize", t), $(".sidebar-control").on("click", t)
        }
        var r = d3.select(t),
            i = {
                top: 5,
                right: 30,
                bottom: 30,
                left: 50
            },
            s = r.node().getBoundingClientRect().width - i.left - i.right,
            e = e - i.top - i.bottom,
            l = d3.tip().attr("class", "d3-tip").html(function(t) {
                return "<ul class='list-unstyled mb-5'><li><div class='text-size-base mt-5 mb-5'><i class='icon-circle-left2 position-left'></i>" + t.name + " app</div></li><li>Sales: &nbsp;<span class='text-semibold pull-right'>" + t.value + "</span></li><li>Revenue: &nbsp; <span class='text-semibold pull-right'>$" + (25 * t.value).toFixed(2) + "</span></li></ul>"
            }),
            o = d3.time.format("%Y/%m/%d").parse,
            d = (d3.time.format("%b %d, '%y"), ["#4CAF50", "#FF5722", "#5C6BC0"]),
            c = d3.scale.ordinal().range(d),
            u = r.append("svg"),
            p = u.attr("width", s + i.left + i.right).attr("height", e + i.top + i.bottom).append("g").attr("transform", "translate(" + i.left + "," + i.top + ")").call(l),
            f = $("#select_date").multiselect({
                buttonClass: "btn btn-link text-semibold",
                enableHTML: !0,
                dropRight: !0,
                onChange: function() {
                    a(), $.uniform.update()
                },
                buttonText: function(t, e) {
                    var a = "";
                    return t.each(function() {
                        a += $(this).html() + ", "
                    }), '<span class="status-mark border-warning position-left"></span>' + a.substr(0, a.length - 2)
                }
            });
        $(".multiselect-container input").uniform({
            radioClass: "choice"
        }), d3.csv("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/app_sales.csv", function(t, e) {
            formatted = e, n()
        });
        var h;
        d3.select(window).on("keydown", function() {
            h = d3.event.altKey
        }).on("keyup", function() {
            h = !1
        })
    }

    function a() {
        d3.csv("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/app_sales_heatmap.csv", function(t, e) {
            function a() {
                width = l.node().getBoundingClientRect().width - margin.left - margin.right, gridSize = width / new Date(e[e.length - 1].date).getHours(), height = (rowGap + gridSize) * d3.max(r, function(t, e) {
                    return e + 1
                }) - margin.top, u.attr("width", width + margin.left + margin.right).attr("height", height + margin.bottom), p.attr("width", width + margin.left + margin.right).attr("height", height + margin.bottom), o.range([0, width]), p.selectAll(".hour-group").attr("transform", function(t, e) {
                    return "translate(0, " + (gridSize + rowGap) * e + ")"
                }), p.selectAll(".heatmap-hour").attr("width", gridSize).attr("height", gridSize).attr("x", function(t, e) {
                    return o(t.date)
                }), p.selectAll(".legend-group").attr("transform", "translate(" + (width / 2 - buckets * gridSize / 2) + "," + (height + margin.bottom - margin.top) + ")"), p.selectAll(".sales-count").attr("x", width), p.selectAll(".heatmap-legend-item").attr("width", gridSize).attr("x", function(t, e) {
                    return gridSize * e
                }), p.selectAll(".max-legend-value").attr("x", buckets * gridSize + 10)
            }
            var n = d3.nest().key(function(t) {
                    return t.app
                }),
                r = n.entries(e),
                i = d3.time.format("%Y/%m/%d %H:%M"),
                s = d3.time.format("%H:%M");
            e.forEach(function(t, e) {
                t.date = i.parse(t.date), t.value = +t.value
            });
            var l = d3.select("#sales-heatmap");
            margin = {
                top: 20,
                right: 0,
                bottom: 30,
                left: 0
            }, width = l.node().getBoundingClientRect().width - margin.left - margin.right, gridSize = width / new Date(e[e.length - 1].date).getHours(), rowGap = 40, height = (rowGap + gridSize) * d3.max(r, function(t, e) {
                return e + 1
            }) - margin.top, buckets = 5, colors = ["#DCEDC8", "#C5E1A5", "#9CCC65", "#7CB342", "#558B2F"];
            var o = d3.time.scale().range([0, width]),
                d = d3.scale.linear().range([height, 0]),
                c = d3.scale.quantile().domain([0, buckets - 1, d3.max(e, function(t) {
                    return t.value
                })]).range(colors);
            o.domain([new Date(e[0].date), d3.time.hour.offset(new Date(e[e.length - 1].date), 1)]), d.domain([0, d3.max(e, function(t) {
                return t.app
            })]);
            var u = l.append("svg"),
                p = u.attr("width", width + margin.left + margin.right).attr("height", height + margin.bottom).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")"),
                f = p.selectAll(".hour-group").data(r).enter().append("g").attr("class", "hour-group").attr("transform", function(t, e) {
                    return "translate(0, " + (gridSize + rowGap) * e + ")"
                });
            f.append("text").attr("class", "app-label").attr("x", 0).attr("y", -(margin.top / 2)).text(function(t, e) {
                return t.key
            }), f.append("text").attr("class", "sales-count").attr("x", width).attr("y", -(margin.top / 2)).style("text-anchor", "end").text(function(t, e) {
                return d3.sum(t.values, function(t) {
                    return t.value
                }) + " sales today"
            });
            var h = f.selectAll(".heatmap-hour").data(function(t) {
                return t.values
            }).enter().append("rect").attr("x", function(t, e) {
                return o(t.date)
            }).attr("y", 0).attr("class", "heatmap-hour").attr("width", gridSize).attr("height", gridSize).style("fill", "#fff").style("stroke", "#fff").style("cursor", "pointer").style("shape-rendering", "crispEdges");
            h.transition().duration(250).delay(function(t, e) {
                return 20 * e
            }).style("fill", function(t) {
                return c(t.value)
            }), f.each(function(t) {
                h.on("mouseover", function(t, e) {
                    d3.select(this).style("opacity", .75), d3.select(this.parentNode).select(".sales-count").text(function(t) {
                        return t.values[e].value + " sales at " + s(t.values[e].date)
                    })
                }).on("mouseout", function(t, e) {
                    d3.select(this).style("opacity", 1), d3.select(this.parentNode).select(".sales-count").text(function(t, e) {
                        return d3.sum(t.values, function(t) {
                            return t.value
                        }) + " sales today"
                    })
                })
            });
            var m, g;
            e.forEach(function(t, a) {
                g = d3.max(e, function(t) {
                    return t.value
                }), m = d3.min(e, function(t) {
                    return t.value
                })
            });
            var y = p.append("g").attr("class", "legend-group").attr("width", width).attr("transform", "translate(" + (width / 2 - buckets * gridSize / 2) + "," + (height + (margin.bottom - margin.top)) + ")"),
                v = y.selectAll(".heatmap-legend").data([0].concat(c.quantiles()), function(t) {
                    return t
                }).enter().append("g").attr("class", "heatmap-legend");
            v.append("rect").attr("class", "heatmap-legend-item").attr("x", function(t, e) {
                return gridSize * e
            }).attr("y", -8).attr("width", gridSize).attr("height", 5).style("stroke", "#fff").style("shape-rendering", "crispEdges").style("fill", function(t, e) {
                return colors[e]
            }), y.append("text").attr("class", "min-legend-value").attr("x", -10).attr("y", -2).style("text-anchor", "end").style("font-size", 11).style("fill", "#999").text(m), y.append("text").attr("class", "max-legend-value").attr("x", buckets * gridSize + 10).attr("y", -2).style("font-size", 11).style("fill", "#999").text(g), $(window).on("resize", a), $(".sidebar-control").on("click", a)
        })
    }

    function n(t, e, a) {
        var n = d3.select(t),
            r = {
                top: 20,
                right: 35,
                bottom: 40,
                left: 35
            },
            i = n.node().getBoundingClientRect().width - r.left - r.right,
            e = e - r.top - r.bottom,
            s = d3.time.format("%Y-%m-%d").parse,
            l = d3.bisector(function(t) {
                return t.date
            }).left,
            o = d3.time.format("%b %d"),
            d = n.append("svg"),
            c = d.attr("width", i + r.left + r.right).attr("height", e + r.top + r.bottom).append("g").attr("transform", "translate(" + r.left + "," + r.top + ")"),
            u = d3.svg.area().x(function(t) {
                return p(t.date)
            }).y0(e).y1(function(t) {
                return f(t.value)
            }).interpolate("monotone"),
            p = d3.time.scale().range([0, i]),
            f = d3.scale.linear().range([e, 0]),
            h = d3.svg.axis().scale(p).orient("bottom").ticks(d3.time.days, 6).innerTickSize(4).tickPadding(8).tickFormat(d3.time.format("%b %d"));
        d3.json("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/monthly_sales.json", function(t, m) {
            function g() {
                var t = d3.mouse(this),
                    a = t[0],
                    i = (t[1], p.invert(a)),
                    s = l(m, i),
                    d = m[s - 1],
                    c = m[s],
                    u = i - d.date > c.date - i ? c : d;
                w.attr("transform", "translate(" + p(u.date) + "," + e + ")"), k.attr("transform", "translate(" + p(u.date) + "," + f(u.value) + ")"), a >= n.node().getBoundingClientRect().width - A.select("text").node().getBoundingClientRect().width - r.right - r.left ? A.select("text").attr("text-anchor", "end").attr("x", function() {
                    return p(u.date) - 15 + "px"
                }).text(o(u.date) + " - " + u.value + " sales") : A.select("text").attr("text-anchor", "start").attr("x", function() {
                    return p(u.date) + 15 + "px"
                }).text(o(u.date) + " - " + u.value + " sales")
            }

            function y() {
                i = n.node().getBoundingClientRect().width - r.left - r.right, d.attr("width", i + r.left + r.right), c.attr("width", i + r.left + r.right), p.range([0, i]), c.selectAll(".d3-axis-horizontal").call(h), c.selectAll(".d3-axis-subticks").attr("x1", p).attr("x2", p), c.selectAll(".d3-area").datum(m).attr("d", u), c.selectAll(".d3-crosshair-overlay").attr("width", i)
            }
            if (t) return console.error(t);
            m.forEach(function(t) {
                t.date = s(t.date), t.value = +t.value
            });
            var v = d3.max(m, function(t) {
                    return t.value
                }),
                x = m.map(function(t) {
                    return {
                        date: t.date,
                        value: 0
                    }
                });
            p.domain(d3.extent(m, function(t, e) {
                return t.date
            })), f.domain([0, d3.max(m, function(t) {
                return t.value
            })]);
            var b = c.append("g").attr("class", "d3-axis d3-axis-horizontal d3-axis-solid").attr("transform", "translate(0," + e + ")").call(h);
            b.selectAll(".d3-axis-subticks").data(p.ticks(d3.time.days), function(t) {
                return t
            }).enter().append("line").attr("class", "d3-axis-subticks").attr("y1", 0).attr("y2", 4).attr("x1", p).attr("x2", p), c.append("path").datum(m).attr("class", "d3-area").attr("d", u).style("fill", a).transition().duration(1e3).attrTween("d", function() {
                var t = d3.interpolateArray(x, m);
                return function(e) {
                    return u(t(e))
                }
            });
            var w = c.append("g").attr("class", "d3-crosshair-line").style("display", "none");
            w.append("line").attr("class", "vertical-crosshair").attr("y1", 0).attr("y2", -v).style("stroke", "#e5e5e5").style("shape-rendering", "crispEdges");
            var k = c.append("g").attr("class", "d3-crosshair-pointer").style("display", "none");
            k.append("circle").attr("r", 3).style("fill", "#fff").style("stroke", a).style("stroke-width", 1);
            var A = c.append("g").attr("class", "d3-crosshair-text").style("display", "none");
            A.append("text").attr("dy", -10).style("font-size", 12), c.append("rect").attr("class", "d3-crosshair-overlay").style("fill", "none").style("pointer-events", "all").attr("width", i).attr("height", e).on("mouseover", function() {
                k.style("display", null), w.style("display", null), A.style("display", null)
            }).on("mouseout", function() {
                k.style("display", "none"), w.style("display", "none"), A.style("display", "none")
            }).on("mousemove", g), $(window).on("resize", y), $(".sidebar-control").on("click", y)
        })
    }

    function r(t, e, a) {
        var n = d3.select(t),
            r = {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            },
            i = n.node().getBoundingClientRect().width - r.left - r.right,
            e = e - r.top - r.bottom,
            s = d3.time.format("%Y-%m-%d").parse,
            l = n.append("svg"),
            o = l.attr("width", i + r.left + r.right).attr("height", e + r.top + r.bottom).append("g").attr("transform", "translate(" + r.left + "," + r.top + ")"),
            d = d3.svg.area().x(function(t) {
                return c(t.date)
            }).y0(e).y1(function(t) {
                return u(t.value)
            }).interpolate("monotone"),
            c = d3.time.scale().range([0, i]),
            u = d3.scale.linear().range([e, 0]);
        d3.json("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/monthly_sales.json", function(t, e) {
            function p() {
                i = n.node().getBoundingClientRect().width - r.left - r.right, l.attr("width", i + r.left + r.right), o.attr("width", i + r.left + r.right), c.range([0, i]), o.selectAll(".d3-area").datum(e).attr("d", d)
            }
            if (t) return console.error(t);
            e.forEach(function(t) {
                t.date = s(t.date), t.value = +t.value
            });
            var f = (d3.max(e, function(t) {
                return t.value
            }), e.map(function(t) {
                return {
                    date: t.date,
                    value: 0
                }
            }));
            c.domain(d3.extent(e, function(t, e) {
                return t.date
            })), u.domain([0, d3.max(e, function(t) {
                return t.value
            })]), o.append("path").datum(e).attr("class", "d3-area").style("fill", a).attr("d", d).transition().duration(1e3).attrTween("d", function() {
                var t = d3.interpolateArray(f, e);
                return function(e) {
                    return d(t(e))
                }
            }), $(window).on("resize", p), $(".sidebar-control").on("click", p)
        })
    }

    function i(t, e, a, n, r, i, s, l) {
        function o() {
            A.attr("transform", null).transition().duration(i).ease("linear").attr("transform", "translate(" + m(0) + ",0)"), "area" == e ? A.attr("d", v).attr("class", "d3-area").style("fill", l) : A.attr("d", y).attr("class", "d3-line d3-line-medium").style("stroke", l)
        }

        function d() {
            p = c.node().getBoundingClientRect().width - u.left - u.right, x.attr("width", p + u.left + u.right), b.attr("width", p + u.left + u.right), m.range([0, p]), k.attr("width", p), b.select(".d3-line").attr("d", y), b.select(".d3-area").attr("d", v)
        }
        for (var c = d3.select(t), u = {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            }, p = c.node().getBoundingClientRect().width - u.left - u.right, n = n - u.top - u.bottom, f = [], h = 0; a > h; h++) f.push(Math.floor(Math.random() * a) + 5);
        var m = d3.scale.linear().range([0, p]),
            g = d3.scale.linear().range([n - 5, 5]);
        m.domain([1, a - 3]), g.domain([0, a]);
        var y = d3.svg.line().interpolate(r).x(function(t, e) {
                return m(e)
            }).y(function(t, e) {
                return g(t)
            }),
            v = d3.svg.area().interpolate(r).x(function(t, e) {
                return m(e)
            }).y0(n).y1(function(t) {
                return g(t)
            }),
            x = c.append("svg"),
            b = x.attr("width", p + u.left + u.right).attr("height", n + u.top + u.bottom).append("g").attr("transform", "translate(" + u.left + "," + u.top + ")"),
            w = b.append("defs").append("clipPath").attr("id", function(e, a) {
                return "load-clip-" + t.substring(1)
            }),
            k = w.append("rect").attr("class", "load-clip").attr("width", 0).attr("height", n);
        k.transition().duration(1e3).ease("linear").attr("width", p);
        var A = b.append("g").attr("clip-path", function(e, a) {
            return "url(#load-clip-" + t.substring(1) + ")"
        }).append("path").datum(f).attr("transform", "translate(" + m(0) + ",0)");
        "area" == e ? A.attr("d", v).attr("class", "d3-area").style("fill", l) : A.attr("d", y).attr("class", "d3-line d3-line-medium").style("stroke", l), A.style("opacity", 0).transition().duration(750).style("opacity", 1), setInterval(function() {
            f.push(Math.floor(Math.random() * a) + 5), f.shift(), o()
        }, s), $(window).on("resize", d), $(".sidebar-control").on("click", d)
    }

    function s(t, e) {
        function a() {
            s = r.node().getBoundingClientRect().width - i.left - i.right, u.attr("width", s + i.left + i.right), p.attr("width", s + i.left + i.right), f.range([l, s - l]), y.attr("width", s), p.selectAll(".d3-line").attr("d", m(n)), p.selectAll(".d3-line-circle").attr("cx", m.x()), p.selectAll(".d3-line-guides").attr("x1", function(t, e) {
                return f(t.date)
            }).attr("x2", function(t, e) {
                return f(t.date)
            })
        }
        var n = [{
                date: "04/13/14",
                alpha: "60"
            }, {
                date: "04/14/14",
                alpha: "35"
            }, {
                date: "04/15/14",
                alpha: "65"
            }, {
                date: "04/16/14",
                alpha: "50"
            }, {
                date: "04/17/14",
                alpha: "65"
            }, {
                date: "04/18/14",
                alpha: "20"
            }, {
                date: "04/19/14",
                alpha: "60"
            }],
            r = d3.select(t),
            i = {
                top: 0,
                right: 0,
                bottom: 0,
                left: 0
            },
            s = r.node().getBoundingClientRect().width - i.left - i.right,
            e = e - i.top - i.bottom,
            l = 20,
            o = d3.time.format("%m/%d/%y").parse,
            d = d3.time.format("%a, %B %e"),
            c = d3.tip().attr("class", "d3-tip").html(function(t) {
                return "<ul class='list-unstyled mb-5'><li><div class='text-size-base mt-5 mb-5'><i class='icon-check2 position-left'></i>" + d(t.date) + "</div></li><li>Sales: &nbsp;<span class='text-semibold pull-right'>" + t.alpha + "</span></li><li>Revenue: &nbsp; <span class='text-semibold pull-right'>$" + (25 * t.alpha).toFixed(2) + "</span></li></ul>"
            }),
            u = r.append("svg"),
            p = u.attr("width", s + i.left + i.right).attr("height", e + i.top + i.bottom).append("g").attr("transform", "translate(" + i.left + "," + i.top + ")").call(c);
        n.forEach(function(t) {
            t.date = o(t.date), t.alpha = +t.alpha
        });
        var f = d3.time.scale().range([l, s - l]),
            h = d3.scale.linear().range([e, 5]);
        f.domain(d3.extent(n, function(t) {
            return t.date
        })), h.domain([0, d3.max(n, function(t) {
            return Math.max(t.alpha)
        })]);
        var m = d3.svg.line().x(function(t) {
                return f(t.date)
            }).y(function(t) {
                return h(t.alpha)
            }),
            g = p.append("defs").append("clipPath").attr("id", "clip-line-small"),
            y = g.append("rect").attr("class", "clip").attr("width", 0).attr("height", e);
        y.transition().duration(1e3).ease("linear").attr("width", s);
        p.append("path").attr({
            d: m(n),
            "clip-path": "url(#clip-line-small)",
            "class": "d3-line d3-line-medium"
        }).style("stroke", "#fff");
        p.select(".line-tickets").transition().duration(1e3).ease("linear");
        var v = p.append("g").selectAll(".d3-line-guides-group").data(n);
        v.enter().append("line").attr("class", "d3-line-guides").attr("x1", function(t, e) {
            return f(t.date)
        }).attr("y1", function(t, a) {
            return e
        }).attr("x2", function(t, e) {
            return f(t.date)
        }).attr("y2", function(t, a) {
            return e
        }).style("stroke", "rgba(255,255,255,0.3)").style("stroke-dasharray", "4,2").style("shape-rendering", "crispEdges"), v.transition().duration(1e3).delay(function(t, e) {
            return 150 * e
        }).attr("y2", function(t, e) {
            return h(t.alpha)
        });
        var x = p.insert("g").selectAll(".d3-line-circle").data(n).enter().append("circle").attr("class", "d3-line-circle d3-line-circle-medium").attr("cx", m.x()).attr("cy", m.y()).attr("r", 3).style("stroke", "#fff").style("fill", "#29B6F6");
        x.style("opacity", 0).transition().duration(250).ease("linear").delay(1e3).style("opacity", 1), x.on("mouseover", function(t) {
            c.offset([-10, 0]).show(t), d3.select(this).transition().duration(250).attr("r", 4)
        }).on("mouseout", function(t) {
            c.hide(t), d3.select(this).transition().duration(250).attr("r", 3)
        }), d3.select(x[0][0]).on("mouseover", function(t) {
            c.offset([0, 10]).direction("e").show(t), d3.select(this).transition().duration(250).attr("r", 4)
        }).on("mouseout", function(t) {
            c.direction("n").hide(t), d3.select(this).transition().duration(250).attr("r", 3)
        }), d3.select(x[0][x.size() - 1]).on("mouseover", function(t) {
            c.offset([0, -10]).direction("w").show(t), d3.select(this).transition().duration(250).attr("r", 4)
        }).on("mouseout", function(t) {
            c.direction("n").hide(t), d3.select(this).transition().duration(250).attr("r", 3)
        }), $(window).on("resize", a), $(".sidebar-control").on("click", a)
    }

    function l(t, e, a, n) {
        function r() {
            var t = d3.interpolate(0, d);
            return function(e) {
                var a = d / (100 / e),
                    n = c.endAngle(o * a);
                return c(t(n))
            }
        }
        var i = d3.select(t),
            s = 2,
            l = Math.min(e / 2, a / 2) - s,
            o = 2 * Math.PI,
            d = $(t).data("progress"),
            c = d3.svg.arc().startAngle(0).innerRadius(0).outerRadius(l).endAngle(function(t) {
                return t.value / t.size * 2 * Math.PI
            }),
            u = i.append("svg"),
            p = u.attr("width", e).attr("height", a).append("g").attr("transform", "translate(" + e / 2 + "," + a / 2 + ")"),
            f = p.append("g").attr("class", "progress-meter");
        f.append("path").attr("d", c.endAngle(o)).style("fill", "#fff").style("stroke", n).style("stroke-width", 1.5);
        var h = f.append("path").style("fill", n);
        h.transition().ease("cubic-out").duration(2500).attrTween("d", r)
    }

    function o(t, e) {
        var a = [{
                browser: "Google Adwords",
                icon: "<i class='icon-google position-left'></i>",
                value: 1047,
                color: "#66BB6A"
            }, {
                browser: "Social media",
                icon: "<i class='icon-share4 position-left'></i>",
                value: 2948,
                color: "#9575CD"
            }, {
                browser: "Youtube video",
                icon: "<i class='icon-youtube position-left'></i>",
                value: 3909,
                color: "#FF7043"
            }],
            n = d3.select(t),
            r = 2,
            i = e / 2 - r,
            s = d3.sum(a, function(t) {
                return t.value
            }),
            l = d3.tip().attr("class", "d3-tip").offset([-10, 0]).direction("e").html(function(t) {
                return "<ul class='list-unstyled mb-5'><li><div class='text-size-base mb-5 mt-5'>" + t.data.icon + t.data.browser + "</div></li><li>Visits: &nbsp;<span class='text-semibold pull-right'>" + t.value + "</span></li><li>Share: &nbsp;<span class='text-semibold pull-right'>" + (100 / (s / t.value)).toFixed(2) + "%</span></li></ul>"
            }),
            o = n.append("svg").call(l),
            d = o.attr("width", e).attr("height", e).append("g").attr("transform", "translate(" + e / 2 + "," + e / 2 + ")"),
            c = d3.layout.pie().sort(null).startAngle(Math.PI).endAngle(3 * Math.PI).value(function(t) {
                return t.value
            }),
            u = d3.svg.arc().outerRadius(i).innerRadius(i / 2),
            p = d.selectAll(".d3-arc").data(c(a)).enter().append("g").attr("class", "d3-arc").style("stroke", "#fff").style("cursor", "pointer"),
            f = p.append("path").style("fill", function(t) {
                return t.data.color
            });
        f.on("mouseover", function(t, e) {
            d3.select(this).transition().duration(500).ease("elastic").attr("transform", function(t) {
                t.midAngle = (t.endAngle - t.startAngle) / 2 + t.startAngle;
                var e = Math.sin(t.midAngle) * r,
                    a = -Math.cos(t.midAngle) * r;
                return "translate(" + e + "," + a + ")"
            })
        }).on("mousemove", function(t) {
            l.show(t).style("top", d3.event.pageY - 40 + "px").style("left", d3.event.pageX + 30 + "px")
        }).on("mouseout", function(t, e) {
            d3.select(this).transition().duration(500).ease("bounce").attr("transform", "translate(0,0)"), l.hide(t)
        }), f.transition().delay(function(t, e) {
            return 500 * e
        }).duration(500).attrTween("d", function(t) {
            var e = d3.interpolate(t.startAngle, t.endAngle);
            return function(a) {
                return t.endAngle = e(a), u(t)
            }
        })
    }

    function d(t, e) {
        var a = [{
                status: "Active campaigns",
                icon: "<span class='status-mark border-blue-300 position-left'></span>",
                value: 439,
                color: "#29B6F6"
            }, {
                status: "Closed campaigns",
                icon: "<span class='status-mark border-danger-300 position-left'></span>",
                value: 290,
                color: "#EF5350"
            }, {
                status: "Pending campaigns",
                icon: "<span class='status-mark border-success-300 position-left'></span>",
                value: 190,
                color: "#81C784"
            }, {
                status: "Campaigns on hold",
                icon: "<span class='status-mark border-grey-300 position-left'></span>",
                value: 148,
                color: "#999"
            }],
            n = d3.select(t),
            r = 2,
            i = e / 2 - r,
            s = d3.sum(a, function(t) {
                return t.value
            }),
            l = d3.tip().attr("class", "d3-tip").offset([-10, 0]).direction("e").html(function(t) {
                return "<ul class='list-unstyled mb-5'><li><div class='text-size-base mb-5 mt-5'>" + t.data.icon + t.data.status + "</div></li><li>Total: &nbsp;<span class='text-semibold pull-right'>" + t.value + "</span></li><li>Share: &nbsp;<span class='text-semibold pull-right'>" + (100 / (s / t.value)).toFixed(2) + "%</span></li></ul>"
            }),
            o = n.append("svg").call(l),
            d = o.attr("width", e).attr("height", e).append("g").attr("transform", "translate(" + e / 2 + "," + e / 2 + ")"),
            c = d3.layout.pie().sort(null).startAngle(Math.PI).endAngle(3 * Math.PI).value(function(t) {
                return t.value
            }),
            u = d3.svg.arc().outerRadius(i).innerRadius(i / 2),
            p = d.selectAll(".d3-arc").data(c(a)).enter().append("g").attr("class", "d3-arc").style("stroke", "#fff").style("cursor", "pointer"),
            f = p.append("path").style("fill", function(t) {
                return t.data.color
            });
        f.on("mouseover", function(t, e) {
            d3.select(this).transition().duration(500).ease("elastic").attr("transform", function(t) {
                t.midAngle = (t.endAngle - t.startAngle) / 2 + t.startAngle;
                var e = Math.sin(t.midAngle) * r,
                    a = -Math.cos(t.midAngle) * r;
                return "translate(" + e + "," + a + ")"
            })
        }).on("mousemove", function(t) {
            l.show(t).style("top", d3.event.pageY - 40 + "px").style("left", d3.event.pageX + 30 + "px")
        }).on("mouseout", function(t, e) {
            d3.select(this).transition().duration(500).ease("bounce").attr("transform", "translate(0,0)"), l.hide(t)
        }), f.transition().delay(function(t, e) {
            return 500 * e
        }).duration(500).attrTween("d", function(t) {
            var e = d3.interpolate(t.startAngle, t.endAngle);
            return function(a) {
                return t.endAngle = e(a), u(t)
            }
        })
    }

    function c(t, e) {
        var a = [{
                status: "Pending tickets",
                icon: "<i class='status-mark border-blue-300 position-left'></i>",
                value: 295,
                color: "#29B6F6"
            }, {
                status: "Resolved tickets",
                icon: "<i class='status-mark border-success-300 position-left'></i>",
                value: 189,
                color: "#66BB6A"
            }, {
                status: "Closed tickets",
                icon: "<i class='status-mark border-danger-300 position-left'></i>",
                value: 277,
                color: "#EF5350"
            }],
            n = d3.select(t),
            r = 2,
            i = e / 2 - r,
            s = d3.sum(a, function(t) {
                return t.value
            }),
            l = d3.tip().attr("class", "d3-tip").offset([-10, 0]).direction("e").html(function(t) {
                return "<ul class='list-unstyled mb-5'><li><div class='text-size-base mb-5 mt-5'>" + t.data.icon + t.data.status + "</div></li><li>Total: &nbsp;<span class='text-semibold pull-right'>" + t.value + "</span></li><li>Share: &nbsp;<span class='text-semibold pull-right'>" + (100 / (s / t.value)).toFixed(2) + "%</span></li></ul>"
            }),
            o = n.append("svg").call(l),
            d = o.attr("width", e).attr("height", e).append("g").attr("transform", "translate(" + e / 2 + "," + e / 2 + ")"),
            c = d3.layout.pie().sort(null).startAngle(Math.PI).endAngle(3 * Math.PI).value(function(t) {
                return t.value
            }),
            u = d3.svg.arc().outerRadius(i).innerRadius(i / 2),
            p = d.selectAll(".d3-arc").data(c(a)).enter().append("g").attr("class", "d3-arc").style("stroke", "#fff").style("cursor", "pointer"),
            f = p.append("path").style("fill", function(t) {
                return t.data.color
            });
        f.on("mouseover", function(t, e) {
            d3.select(this).transition().duration(500).ease("elastic").attr("transform", function(t) {
                t.midAngle = (t.endAngle - t.startAngle) / 2 + t.startAngle;
                var e = Math.sin(t.midAngle) * r,
                    a = -Math.cos(t.midAngle) * r;
                return "translate(" + e + "," + a + ")"
            })
        }).on("mousemove", function(t) {
            l.show(t).style("top", d3.event.pageY - 40 + "px").style("left", d3.event.pageX + 30 + "px")
        }).on("mouseout", function(t, e) {
            d3.select(this).transition().duration(500).ease("bounce").attr("transform", "translate(0,0)"), l.hide(t)
        }), f.transition().delay(function(t, e) {
            return 500 * e
        }).duration(500).attrTween("d", function(t) {
            var e = d3.interpolate(t.startAngle, t.endAngle);
            return function(a) {
                return t.endAngle = e(a), u(t)
            }
        })
    }

    function u(t, e, a, n, r, i, s, l, o) {
        function d() {
            b.attr("height", 0).attr("y", a).transition().attr("height", function(t) {
                return y(t)
            }).attr("y", function(t) {
                return a - y(t)
            }).delay(function(t, e) {
                return e * s
            }).duration(i).ease(r)
        }

        function c() {
            b.attr("height", function(t) {
                return y(t)
            }).attr("y", function(t) {
                return a - y(t)
            })
        }

        function u() {
            m = h.node().getBoundingClientRect().width, v.attr("width", m), x.attr("width", m), g.rangeBands([0, m], .3), x.selectAll(".d3-random-bars").attr("width", g.rangeBand()).attr("x", function(t, e) {
                return g(e)
            })
        }
        for (var p = [], f = 0; e > f; f++) p.push(Math.round(10 * Math.random()) + 10);
        var h = d3.select(t),
            m = h.node().getBoundingClientRect().width,
            g = d3.scale.ordinal().rangeBands([0, m], .3),
            y = d3.scale.linear().range([0, a]);
        g.domain(d3.range(0, p.length)), y.domain([0, d3.max(p)]);
        var v = h.append("svg"),
            x = v.attr("width", m).attr("height", a).append("g"),
            b = x.selectAll("rect").data(p).enter().append("rect").attr("class", "d3-random-bars").attr("width", g.rangeBand()).attr("x", function(t, e) {
                return g(e)
            }).style("fill", l),
            w = d3.tip().attr("class", "d3-tip").offset([-10, 0]);
        ("hours" == o || "goal" == o || "members" == o) && b.call(w).on("mouseover", w.show).on("mouseout", w.hide), "hours" == o && w.html(function(t, e) {
            return "<div class='text-center'><h6 class='no-margin'>" + t + "</h6><span class='text-size-small'>meetings</span><div class='text-size-small'>" + e + ":00</div></div>"
        }), "goal" == o && w.html(function(t, e) {
            return "<div class='text-center'><h6 class='no-margin'>" + t + "</h6><span class='text-size-small'>statements</span><div class='text-size-small'>" + e + ":00</div></div>"
        }), "members" == o && w.html(function(t, e) {
            return "<div class='text-center'><h6 class='no-margin'>" + t + "0</h6><span class='text-size-small'>members</span><div class='text-size-small'>" + e + ":00</div></div>"
        }), n ? d() : c(), $(window).on("resize", u), $(".sidebar-control").on("click", u)
    }

    function p(t, e, a, n, r, i, s, l) {
        function o(t) {
            w.attr("d", b.endAngle(f * t)), k.attr("d", b.endAngle(f * t)), A.text(h(t))
        }
        var d = d3.select(t),
            c = 0,
            u = 32,
            p = r,
            f = 2 * Math.PI,
            h = d3.format(".0%"),
            m = 2 * e,
            g = Math.abs((p - c) / .01),
            y = c > p ? -.01 : .01,
            v = d.append("svg"),
            x = v.attr("width", m).attr("height", m).append("g").attr("transform", "translate(" + m / 2 + "," + m / 2 + ")"),
            b = d3.svg.arc().startAngle(0).innerRadius(e).outerRadius(e - a);
        x.append("path").attr("class", "d3-progress-background").attr("d", b.endAngle(f)).style("fill", "#eee");
        var w = x.append("path").attr("class", "d3-progress-foreground").attr("filter", "url(#blur)").style("fill", n).style("stroke", n),
            k = x.append("path").attr("class", "d3-progress-front").style("fill", n).style("fill-opacity", 1),
            A = d3.select(t).append("h2").attr("class", "mt-15 mb-5");
        d3.select(t).append("i").attr("class", i + " counter-icon").attr("style", "top: " + (m - u) / 2 + "px"), d3.select(t).append("div").text(s), d3.select(t).append("div").attr("class", "text-size-small text-muted").text(l);
        var z = c;
        ! function C() {
            o(z), g > 0 && (g--, z += y, setTimeout(C, 10))
        }()
    }

    function f(t, e) {
        function a() {
            function t(t) {
                return t.ranges
            }

            function e(t) {
                return t.markers
            }

            function a(t) {
                return t.measures
            }

            function n(t) {
                return function(e) {
                    return "translate(" + t(e) + ",0)"
                }
            }

            function r(t) {
                var e = t(0);
                return function(a) {
                    return Math.abs(t(a) - e)
                }
            }
            d3.bullet = function() {
                function i(t) {
                    t.each(function(t, e) {
                        function a() {
                            l = d3.select("#bullets").node().getBoundingClientRect().width - s.left - s.right, w = r(v), v.range(d ? [l, 0] : [0, l]), y.selectAll(".bullet-measure").attr("width", w).attr("x", d ? v : 0), y.selectAll(".bullet-range").attr("width", w).attr("x", d ? v : 0), y.selectAll(".bullet-marker").attr("x1", v).attr("x2", v), y.selectAll(".bullet-tick").attr("transform", n(v))
                        }
                        var i = u.call(this, t, e).slice().sort(d3.descending),
                            o = p.call(this, t, e).slice().sort(d3.descending),
                            g = f.call(this, t, e).slice().sort(d3.descending),
                            y = d3.select(this),
                            v = d3.scale.linear().domain([0, Math.max(i[0], o[0], g[0])]).range(d ? [l, 0] : [0, l]),
                            x = this.__chart__ || d3.scale.linear().domain([0, 1 / 0]).range(v.range());
                        this.__chart__ = v;
                        var b = r(x),
                            w = r(v),
                            k = y.selectAll(".bullet-range").data(i);
                        k.enter().append("rect").attr("class", function(t, e) {
                            return "bullet-range bullet-range-" + (e + 1)
                        }).attr("width", b).attr("height", h).attr("rx", 2).attr("x", d ? x : 0).transition().duration(c).attr("width", w).attr("x", d ? v : 0), k.transition().duration(c).attr("x", d ? v : 0).attr("width", w).attr("height", h);
                        var A = y.selectAll(".bullet-measure").data(g);
                        A.enter().append("rect").attr("class", function(t, e) {
                            return "bullet-measure bullet-measure-" + (e + 1)
                        }).attr("width", b).attr("height", h / 5).attr("x", d ? x : 0).attr("y", h / 2.5).style("shape-rendering", "crispEdges"), A.transition().duration(c).attr("width", w).attr("x", d ? v : 0), A.transition().duration(c).attr("width", w).attr("height", h / 5).attr("x", d ? v : 0).attr("y", h / 2.5);
                        var z = y.selectAll(".bullet-marker").data(o);
                        z.enter().append("line").attr("class", function(t, e) {
                            return "bullet-marker bullet-marker-" + (e + 1)
                        }).attr("x1", x).attr("x2", x).attr("y1", h / 6).attr("y2", 5 * h / 6), z.transition().duration(c).attr("x1", v).attr("x2", v), z.transition().duration(c).attr("x1", v).attr("x2", v).attr("y1", h / 6).attr("y2", 5 * h / 6);
                        var C = m || v.tickFormat(8),
                            M = y.selectAll(".bullet-tick").data(v.ticks(8), function(t) {
                                return this.textContent || C(t)
                            }),
                            B = M.enter().append("g").attr("class", "bullet-tick").attr("transform", n(x)).style("opacity", 1e-6);
                        B.append("line").attr("y1", h).attr("y2", 7 * h / 6 + 3), B.append("text").attr("text-anchor", "middle").attr("dy", "1em").attr("y", 7 * h / 6 + 4).text(C), B.transition().duration(c).attr("transform", n(v)).style("opacity", 1);
                        var F = M.transition().duration(c).attr("transform", n(v)).style("opacity", 1);
                        F.select("line").attr("y1", h + 3).attr("y2", 7 * h / 6 + 3), F.select("text").attr("y", 7 * h / 6 + 4), M.exit().transition().duration(c).attr("transform", n(v)).style("opacity", 1e-6).remove(), $(window).on("resize", a), $(".sidebar-control").on("click", a)
                    }), d3.timer.flush()
                }
                var o = "left",
                    d = !1,
                    c = 750,
                    u = t,
                    p = e,
                    f = a,
                    h = 30,
                    m = null;
                return i.orient = function(t) {
                    return arguments.length ? (o = t, d = "right" == o || "bottom" == o, i) : o
                }, i.ranges = function(t) {
                    return arguments.length ? (u = t, i) : u
                }, i.markers = function(t) {
                    return arguments.length ? (p = t, i) : p
                }, i.measures = function(t) {
                    return arguments.length ? (f = t, i) : f
                }, i.width = function(t) {
                    return arguments.length ? (l = t, i) : l
                }, i.height = function(t) {
                    return arguments.length ? (h = t, i) : h
                }, i.tickFormat = function(t) {
                    return arguments.length ? (m = t, i) : m
                }, i.duration = function(t) {
                    return arguments.length ? (c = t, i) : c
                }, i
            }
        }

        function n(t) {
            return t.randomizer || (t.randomizer = r(t)), t.ranges = t.ranges.map(t.randomizer), t.markers = t.markers.map(t.randomizer), t.measures = t.measures.map(t.randomizer), t
        }

        function r(t) {
            var e = .2 * d3.max(t.ranges);
            return function(t) {
                return Math.max(0, t + e * (Math.random() - .5))
            }
        }
        a();
        var i = d3.select(t),
            s = {
                top: 20,
                right: 10,
                bottom: 35,
                left: 10
            },
            l = l = i.node().getBoundingClientRect().width - s.left - s.right,
            e = e - s.top - s.bottom,
            o = d3.bullet().width(l).height(e);
        d3.json("http://demo.interface.club/limitless/layout_1/LTR/default/assets/demo_data/dashboard/bullets.json", function(t, a) {
            function r() {
                l = i.node().getBoundingClientRect().width - s.left - s.right, d.attr("width", l + s.left + s.right), c.attr("width", l + s.left + s.right), c.selectAll(".bullet-subtitle").attr("x", l)
            }
            if (t) return console.error(t);
            var d = i.selectAll("svg").data(a).enter().append("svg"),
                c = d.attr("class", function(t, e) {
                    return "bullet-" + (e + 1)
                }).attr("width", l + s.left + s.right).attr("height", e + s.top + s.bottom).append("g").attr("transform", "translate(" + s.left + "," + s.top + ")").call(o),
                u = c.append("g").style("text-anchor", "start");
            u.append("text").attr("class", "bullet-title").attr("y", -10).text(function(t) {
                return t.title
            }), u.append("text").attr("class", "bullet-subtitle").attr("x", l).attr("y", -10).style("text-anchor", "end").text(function(t) {
                return t.subtitle
            }).style("opacity", 0).transition().duration(500).delay(500).style("opacity", 1);
            var p = function() {
                    c.datum(n).call(o.duration(750))
                },
                f = [];
            f.push(setInterval(function() {
                p()
            }, 5e3));
            var h = document.querySelector(".switcher");
            new Switchery(h);
            h.onchange = function() {
                if (h.checked) f.push(setInterval(function() {
                    p()
                }, 5e3));
                else
                    for (var t = 0; t < f.length; t++) clearInterval(f[t])
            }, $(window).on("resize", r), $(".sidebar-control").on("click", r)
        })
    }
    var h = Array.prototype.slice.call(document.querySelectorAll(".switch"));
    h.forEach(function(t) {
        new Switchery(t, {
            color: "#4CAF50"
        })
    }), $(".daterange-ranges").daterangepicker({
        startDate: moment().subtract("days", 29),
        endDate: moment(),
        minDate: "01/01/2012",
        maxDate: "12/31/2016",
        dateLimit: {
            days: 60
        },
        ranges: {
            Today: [moment(), moment()],
            Yesterday: [moment().subtract("days", 1), moment().subtract("days", 1)],
            "Last 7 Days": [moment().subtract("days", 6), moment()],
            "Last 30 Days": [moment().subtract("days", 29), moment()],
            "This Month": [moment().startOf("month"), moment().endOf("month")],
            "Last Month": [moment().subtract("month", 1).startOf("month"), moment().subtract("month", 1).endOf("month")]
        },
        opens: "left",
        applyClass: "btn-small bg-slate-600 btn-block",
        cancelClass: "btn-small btn-default btn-block",
        format: "MM/DD/YYYY"
    }, function(t, e) {
        $(".daterange-ranges span").html(t.format("MMMM D") + " - " + e.format("MMMM D"))
    }), $(".daterange-ranges span").html(moment().subtract("days", 29).format("MMMM D") + " - " + moment().format("MMMM D")), t("#traffic-sources", 330), e("#app_sales", 255), a(), n("#monthly-sales-stats", 100, "#4DB6AC"), r("#messages-stats", 40, "#5C6BC0"), i("#new-visitors", "line", 30, 35, "basis", 750, 2e3, "#26A69A"), i("#new-sessions", "line", 30, 35, "basis", 750, 2e3, "#FF7043"), i("#total-online", "line", 30, 35, "basis", 750, 2e3, "#5C6BC0"), i("#server-load", "area", 30, 50, "basis", 750, 2e3, "rgba(255,255,255,0.5)"), s("#today-revenue", 50), l("#today-progress", 20, 20, "#7986CB"), l("#yesterday-progress", 20, 20, "#7986CB"), o("#campaigns-donut", 42), d("#campaign-status-pie", 42), c("#tickets-status", 42), u("#hours-available-bars", 24, 40, !0, "elastic", 1200, 50, "#EC407A", "hours"), u("#goal-bars", 24, 40, !0, "elastic", 1200, 50, "#5C6BC0", "goal"), u("#members-online", 24, 50, !0, "elastic", 1200, 50, "rgba(255,255,255,0.5)", "members"), p("#hours-available-progress", 38, 2, "#F06292", .68, "icon-watch text-pink-400", "Hours available", "64% average"), p("#goal-progress", 38, 2, "#5C6BC0", .82, "icon-trophy3 text-indigo-400", "Productivity goal", "87% average"), f("#bullets", 80), $(".table tr").each(function(t) {
        var e = $(this).find(".letter-icon-title"),
            a = e.eq(0).text().charAt(0).toUpperCase(),
            n = $(this).find(".letter-icon");
        n.eq(0).text(a)
    })
});