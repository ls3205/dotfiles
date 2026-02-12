return {
	-- tools
	{
		"mason-org/mason.nvim",
		opts = function(_, opts)
			vim.list_extend(opts.ensure_installed, {
				"stylua",
				"selene",
				"luacheck",
				"shellcheck",
				"shfmt",
				"tailwindcss-language-server",
				"typescript-language-server",
				"css-lsp",
				"python-lsp-server",
			})
		end,
	},

	-- lsp servers
	{
		"neovim/nvim-lspconfig",
		opts = {
			inlay_hints = { enabled = false },
			---@type lspconfig.options
			servers = {
				["*"] = {
					keys = {
						{
							"gd",
							"<cmd>lua vim.lsp.buf.definition()<CR>",
							has = "definition",
						},
					},
				},
				cssls = {},
				tailwindcss = {
					root_dir = function(...)
						return require("lspconfig.util").root_pattern(".git")(...)
					end,
				},
				vtsls = {
					filetypes = {
						"vue",
						"javascript",
						"javascriptreact",
						"javascript.jsx",
						"typescript",
						"typescriptreact",
						"typescript.tsx",
					},
					root_markers = {
						"tsconfig.json",
						"package.json",
						"jsconfig.json",
						".git",
					},
					settings = {
						complete_function_calls = true,
						vtsls = {
							enableMoveToFileCodeAction = true,
							autoUseWorkspaceTsdk = true,
							experimental = {
								maxInlayHintLength = 30,
								completion = {
									enableServerSideFuzzyMatch = true,
								},
							},
							tsserver = {
								globalPlugins = {
									{
										name = "@vue/typescript-plugin",
										location = vim.fn.stdpath("data")
											.. "/mason/packages/vue-language-server"
											.. "/node_modules/@vue/typescript-plugin",
										languages = { "vue" },
										configNamespace = "typescript",
										enableForWorkspaceTypeScriptVersions = true,
									},
								},
							},
						},
						typescript = {
							updateImportsOnFileMove = { enabled = "always" },
							suggest = {
								completeFunctionCalls = true,
							},
							inlayHints = {
								enumMemberValues = { enabled = true },
								functionLikeReturnTypes = { enabled = true },
								parameterNames = { enabled = "literals" },
								parameterTypes = { enabled = true },
								propertyDeclarationTypes = { enabled = true },
								variableTypes = { enabled = false },
							},
						},
						javascript = {
							updateImportsOnFileMove = { enabled = "always" },
						},
					},
				},

				-- tsserver = {
				-- 	root_dir = function(...)
				-- 		return require("lspconfig.util").root_pattern(".git")(...)
				-- 	end,
				-- 	single_file_support = false,
				-- 	plugins = {
				-- 		{
				-- 			name = "@vue/typescript-plugin",
				-- 			location = vim.fn.stdpath("data")
				-- 				.. "/mason/packages/vue-language-server"
				-- 				.. "/node_modules/@vue/typescript-plugin",
				-- 			languages = { "javascript", "typescript", "vue" },
				-- 		},
				-- 	},
				-- 	settings = {
				-- 		typescript = {
				-- 			inlayHints = {
				-- 				includeInlayParameterNameHints = "literal",
				-- 				includeInlayParameterNameHintsWhenArgumentMatchesName = false,
				-- 				includeInlayFunctionParameterTypeHints = true,
				-- 				includeInlayVariableTypeHints = false,
				-- 				includeInlayPropertyDeclarationTypeHints = true,
				-- 				includeInlayFunctionLikeReturnTypeHints = true,
				-- 				includeInlayEnumMemberValueHints = true,
				-- 			},
				-- 		},
				-- 		javascript = {
				-- 			inlayHints = {
				-- 				includeInlayParameterNameHints = "all",
				-- 				includeInlayParameterNameHintsWhenArgumentMatchesName = false,
				-- 				includeInlayFunctionParameterTypeHints = true,
				-- 				includeInlayVariableTypeHints = true,
				-- 				includeInlayPropertyDeclarationTypeHints = true,
				-- 				includeInlayFunctionLikeReturnTypeHints = true,
				-- 				includeInlayEnumMemberValueHints = true,
				-- 			},
				-- 		},
				-- 	},
				-- },
				html = {},
				yamlls = {
					settings = {
						yaml = {
							keyOrdering = false,
						},
					},
				},
				lua_ls = {
					-- enabled = false,
					single_file_support = true,
					settings = {
						Lua = {
							workspace = {
								checkThirdParty = false,
							},
							completion = {
								workspaceWord = true,
								callSnippet = "Both",
							},
							misc = {
								parameters = {
									-- "--log-level=trace",
								},
							},
							hint = {
								enable = true,
								setType = false,
								paramType = true,
								paramName = "Disable",
								semicolon = "Disable",
								arrayIndex = "Disable",
							},
							doc = {
								privateName = { "^_" },
							},
							type = {
								castNumberToInteger = true,
							},
							diagnostics = {
								disable = { "incomplete-signature-doc", "trailing-space" },
								-- enable = false,
								groupSeverity = {
									strong = "Warning",
									strict = "Warning",
								},
								groupFileStatus = {
									["ambiguity"] = "Opened",
									["await"] = "Opened",
									["codestyle"] = "None",
									["duplicate"] = "Opened",
									["global"] = "Opened",
									["luadoc"] = "Opened",
									["redefined"] = "Opened",
									["strict"] = "Opened",
									["strong"] = "Opened",
									["type-check"] = "Opened",
									["unbalanced"] = "Opened",
									["unused"] = "Opened",
								},
								unusedLocalExclude = { "_*" },
							},
							format = {
								enable = false,
								defaultConfig = {
									indent_style = "space",
									indent_size = "2",
									continuation_indent_size = "2",
								},
							},
						},
					},
				},
			},
			setup = {},
		},
	},
	-- {
	-- 	"neovim/nvim-lspconfig",
	-- 	opts = function()
	-- 		local keys = require("lazyvim.plugins.lsp.keymaps").get()
	-- 		vim.list_extend(keys, {
	-- 			{
	-- 				"gd",
	-- 				function()
	-- 					-- DO NOT RESUSE WINDOW
	-- 					require("telescope.builtin").lsp_definitions({ reuse_win = false })
	-- 				end,
	-- 				desc = "Goto Definition",
	-- 				has = "definition",
	-- 			},
	-- 		})
	-- 	end,
	-- },
}
