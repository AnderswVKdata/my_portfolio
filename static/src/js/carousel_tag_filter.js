/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.CarouselTagFilter = publicWidget.Widget.extend({
    selector: ".filter-btn",
    events: {
        "click": "_onClickFilter",
    },

    /**
     * Keep track of active filters
     */
    activeFilters: new Set(),

    /**
     * Handle filter button click
     */
    _onClickFilter(ev) {
        const btn = ev.currentTarget;
        const filter = btn.getAttribute("data-filter");
        const buttons = document.querySelectorAll(".filter-btn");

        if (filter === "all") {
            // Reset filters
            this.activeFilters.clear();

            // Reset button highlights
            buttons.forEach(b => {
                b.classList.remove("bg-primary");
                b.classList.add("bg-secondary");
            });
            btn.classList.remove("bg-secondary");
            btn.classList.add("bg-primary");
        } else {
            // Toggle filter
            if (this.activeFilters.has(filter)) {
                this.activeFilters.delete(filter);
                btn.classList.remove("bg-primary");
                btn.classList.add("bg-secondary");
            } else {
                this.activeFilters.add(filter);
                btn.classList.remove("bg-secondary");
                btn.classList.add("bg-primary");
            }

            // Ensure "All" is reset
            const allBtn = document.querySelector('.filter-btn[data-filter="all"]');
            if (allBtn) {
                allBtn.classList.remove("bg-primary");
                allBtn.classList.add("bg-secondary");
            }
        }

        this._applyFilter();
    },

    /**
     * Apply active filters to carousel
     */
    _applyFilter() {
        const items = document.querySelectorAll(".s_carousel_intro_item");
        const carouselInner = document.querySelector(".carousel-inner");

        if (!carouselInner) {
            return;
        }

        // Hide/show items based on filters
        items.forEach(item => {
            const tags = item.getAttribute("data-tags")?.split(",") || [];
            const matches = [...this.activeFilters].every(f => tags.includes(f));

            if (this.activeFilters.size === 0 || matches) {
                item.style.display = "";
            } else {
                item.style.display = "none";
            }

            item.classList.remove("active");
        });

        // Collect visible items
        const visibleItems = Array.from(items).filter(i => i.style.display !== "none");

        // Ensure only first visible one is active
        if (visibleItems.length > 0) {
            visibleItems[0].classList.add("active");
        }

        // Sync carousel indicators
        const indicators = document.querySelectorAll(".carousel-indicators button");
        indicators.forEach((btn, idx) => {
            if (visibleItems[idx]) {
                btn.style.display = "";
                btn.classList.remove("active");
                if (idx === 0) {
                    btn.classList.add("active");
                    btn.setAttribute("aria-current", "true");
                } else {
                    btn.removeAttribute("aria-current");
                }
            } else {
                btn.style.display = "none";
            }
        });
    },
});
