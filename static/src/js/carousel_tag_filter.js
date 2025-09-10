/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.CarouselTagFilter = publicWidget.Widget.extend({
    selector: ".filter-btn",
    events: { "click": "_onClickFilter" },
    activeFilters: new Set(),

    _onClickFilter(ev) {
        const btn = ev.currentTarget;
        const filter = btn.getAttribute("data-filter");
        const buttons = document.querySelectorAll(".filter-btn");

        if (filter === "all") {
            this.activeFilters.clear();
            buttons.forEach(b => {
                b.classList.remove("bg-primary");
                b.classList.add("bg-secondary");
            });
            btn.classList.remove("bg-secondary");
            btn.classList.add("bg-primary");
        } else {
            if (this.activeFilters.has(filter)) {
                this.activeFilters.delete(filter);
                btn.classList.remove("bg-primary");
                btn.classList.add("bg-secondary");
            } else {
                this.activeFilters.add(filter);
                btn.classList.remove("bg-secondary");
                btn.classList.add("bg-primary");
            }

            const allBtn = document.querySelector('.filter-btn[data-filter="all"]');
            if (allBtn) {
                allBtn.classList.remove("bg-primary");
                allBtn.classList.add("bg-secondary");
            }
        }

        this._applyFilter();
    },

    async _applyFilter() {
        const filters = [...this.activeFilters];

        try {
            const html = await rpc("/portfolio/filter", { tags: filters });
            const wrapper = document.querySelector("#carousel-wrapper");
            if (!wrapper) {
                console.warn("carousel wrapper not found");
                return;
            }

            wrapper.innerHTML = html;

            // locate carousel element inside wrapper
            const carouselEl = wrapper.querySelector(".carousel");
            if (!carouselEl) {
                // nothing to init
                return;
            }

            // ensure carousel has an id; if not, create one and update any data-bs-target attributes inside wrapper
            if (!carouselEl.id) {
                const generatedId = "carousel_" + Math.floor(Math.random() * 1000000);
                carouselEl.id = generatedId;
                wrapper.querySelectorAll("[data-bs-target]").forEach(el => {
                    el.setAttribute("data-bs-target", "#" + generatedId);
                });
            }

            // make sure at least one item has .active
            const firstItem = carouselEl.querySelector(".carousel-item");
            if (firstItem && !carouselEl.querySelector(".carousel-item.active")) {
                firstItem.classList.add("active");
            }

            // ensure indicators count matches items count — if mismatch, rebuild indicators
            const itemsCount = carouselEl.querySelectorAll(".carousel-item").length;
            const indicatorsContainer = carouselEl.querySelector(".carousel-indicators");
            if (indicatorsContainer) {
                const indicators = indicatorsContainer.querySelectorAll("[data-bs-slide-to]");
                if (indicators.length !== itemsCount) {
                    // rebuild indicators to match visible items
                    indicatorsContainer.innerHTML = "";
                    for (let i = 0; i < itemsCount; i++) {
                        const btn = document.createElement("button");
                        btn.type = "button";
                        btn.setAttribute("data-bs-target", "#" + carouselEl.id);
                        btn.setAttribute("data-bs-slide-to", String(i));
                        if (i === 0) {
                            btn.classList.add("active");
                            btn.setAttribute("aria-current", "true");
                        }
                        indicatorsContainer.appendChild(btn);
                    }
                }
            }

            // Initialize carousel safely
            try {
                if (window.bootstrap && window.bootstrap.Carousel) {
                    window.bootstrap.Carousel.getOrCreateInstance(carouselEl);
                } else {
                    // bootstrap may be missing in a minimal bundle; log for debugging
                    console.warn("Bootstrap Carousel is not present on this page.");
                }
            } catch (initErr) {
                console.warn("Carousel initialization error:", initErr);
            }
        } catch (err) {
            console.error("RPC failed:", err);
        }
    },
});
