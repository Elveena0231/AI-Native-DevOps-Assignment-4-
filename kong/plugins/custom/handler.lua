local CustomHandler = {
  PRIORITY = 1000,
  VERSION = "0.1.0",
}

function CustomHandler:access(conf)
  local req_id = kong.request.get_header("x-request-id") or kong.request.get_header("X-Request-Id") or ngx.var.request_id
  if not req_id then
    math.randomseed(ngx.now() * 1000 + ngx.worker.pid())
    req_id = tostring(math.floor(ngx.now())) .. "-" .. tostring(math.random(1000000, 9999999))
  end
  kong.ctx.shared.custom_request_id = req_id
end

function CustomHandler:header_filter(conf)
  local req_id = kong.ctx.shared.custom_request_id
  if req_id then
    kong.response.set_header("X-Custom-Trace", req_id)
  end
end

return CustomHandler
