return {
	"mfussenegger/nvim-jdtls",
	opts = {
		cmd = {
			"jdtls",
		},
	},

	-- setup nvim-jdtls
	config = function(_, opts)
		-- vim api auto-command to start_or_attach this only for java
		vim.api.nvim_create_autocmd("FileType", {
			pattern = "java",
			callback = function()
				vim.uv.os_setenv("JAVA_HOME", "/usr/lib/jvm/java-21-openjdk/")
				-- prints and pcall are there only to give quick feedback if it works.
				-- print("Starting JDTLS...")
				local success, result = pcall(require("jdtls").start_or_attach, opts)
				-- if success then
				-- 	print("JDTLS started successfully")
				-- else
				-- 	print("Error starting JDTLS: " .. tostring(result))
				-- end
			end,
		})
	end,
}
