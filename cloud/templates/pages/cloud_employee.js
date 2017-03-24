frappe.ready(function() {
	$(".btn-cloud-delete-user").click(function() {
		var args = {
			company: $("#company").val(),
			user: $("#user").val(),
		};

		if(!args.user) {
			frappe.msgprint("User Required.");
			return false;
		}

		frappe.call({
			type: "POST",
			method: "cloud.cloud.doctype.cloud_employee.cloud_employee.delete_employee",
			btn: $(".btn-iot-delete-user"),
			args: args,
			callback: function(r) {
				if(!r.exc) {
					if(r.message) {
						frappe.msgprint(r.message);
						setTimeout(function() {
							window.location.href = "/iot_companies/"+args.company;
						}, 2000);
					}
				}
			}
		});

        return false;
	});
});