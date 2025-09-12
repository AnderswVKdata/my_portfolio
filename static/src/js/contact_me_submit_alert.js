/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ContactFormHandler = publicWidget.Widget.extend({
    selector: "#contact-form",   
    events: {
        submit: "_onSubmit",
    },

    async _onSubmit(ev) {
        ev.preventDefault();

        const form = ev.currentTarget;
        const formData = new FormData(form);

        try {
            const resp = await fetch(form.action, {
                method: "POST",
                body: formData,
            });
            if (resp.ok) {
                alert("Thank you for contacting me!");
                form.reset();
            } else {
                alert("Something went wrong. Please try again.");
            }
        } catch (err) {
            console.error("Contact form error:", err);
            alert("Error: could not send message.");
        }
    },
});